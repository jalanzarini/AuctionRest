import json
import pika, os, sys, threading
from flask import Flask, request
from ast import literal_eval
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

leiloes = []
lances = []

'''
Estrutura JSON do lance:
{
    id_leilao: int,
    id_user: int,
    valor_lance: float
}
'''
@app.route("/bid/make", methods=['POST'])
def make_bid():
    data = request.get_json()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=0))
    channel = connection.channel()

    invalidado = channel.queue_declare(queue='lance_invalidado', exclusive=False)
    validado = channel.queue_declare(queue='lance_validado', exclusive=False)
    channel.exchange_declare(exchange='lances', exchange_type='direct')
    channel.queue_bind(exchange='lances', queue=invalidado.method.queue, routing_key='invalidado')
    channel.queue_bind(exchange='lances', queue=validado.method.queue, routing_key='validado')

    handled_leilao = next((leilao for leilao in leiloes if leilao["id"] == data["id_leilao"]), None)
    if not handled_leilao or leiloes[leiloes.index(handled_leilao)]["status"] != "ativo":
        print(f" [ ] Lance ignorado: {data}\n")
        data['status'] = 'ignorado'
        channel.basic_publish(exchange='lances', routing_key='invalidado', body=str(data))
        return 'Lance ignorado: leilão inexistente ou inativo', 404

    elif data["valor_lance"] <= handled_leilao["maior_lance"]:
        print(f" [ ] Lance rejeitado: {data}\n")
        data['status'] = 'rejeitado'
        channel.basic_publish(exchange='lances', routing_key='invalidado', body=str(data))
        return 'Lance rejeitado: valor inferior ao maior lance atual', 400

    else:
        leiloes[leiloes.index(handled_leilao)]["maior_lance"] = data["valor_lance"]
        leiloes[leiloes.index(handled_leilao)]["user_maior_lance"] = data["id_user"]
        data['status'] = 'validado'
        lances.append(data)
        
        with open("logs/lances.log", "w") as f:
            json.dump(lances, f, indent=4)

        print(f" [x] Lance aceito: {data}\n")
        channel.basic_publish(exchange='lances', routing_key='validado', body=str(data))
        return 'Lance processado com sucesso', 200

def main():

    connection1 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=0))
    channel1 = connection1.channel()

    iniciado = channel1.queue_declare(queue='', exclusive=True)
    finalizado = channel1.queue_declare(queue='', exclusive=True)
    vencedor = channel1.queue_declare(queue='', exclusive=True)
    channel1.exchange_declare(exchange='leilao', exchange_type='direct')
    channel1.queue_bind(exchange='leilao', queue=iniciado.method.queue, routing_key='iniciado')
    channel1.queue_bind(exchange='leilao', queue=finalizado.method.queue, routing_key='finalizado')
    channel1.queue_bind(exchange='leilao', queue=vencedor.method.queue, routing_key='vencedor')

    def leilao_iniciado(ch, method, properties, body):
        data = literal_eval(body.decode())
        leiloes.append(data)
        leiloes[-1]["maior_lance"] = data['valor_inicial']
        leiloes[-1]["user_maior_lance"] = 0
        print(f" [x] Leilão {data['id']} iniciado\n")

    def leilao_finalizado(ch, method, properties, body):
        data = literal_eval(body.decode())
        if data['id'] in [leilao['id'] for leilao in leiloes]:
            
            leilao_finalizado = leiloes[[leilao['id'] for leilao in leiloes].index(data['id'])]
            leiloes[leiloes.index(leilao_finalizado)]["status"] = "finalizado"
            
            body = {
                'id_leilao': leilao_finalizado['id'],
                'id_user_vencedor': leilao_finalizado['user_maior_lance'],
                'valor_vencedor': leilao_finalizado['maior_lance']
            }
            channel1.basic_publish(exchange='leilao', routing_key='vencedor', body=str(body))
            print(f" [x] Leilão {data['id']} finalizado\n")
        else:
            print(f" [ ] Leilão {data['id']} não encontrado\n")

    channel1.basic_consume(queue=iniciado.method.queue, on_message_callback=leilao_iniciado, auto_ack=True)
    channel1.basic_consume(queue=finalizado.method.queue, on_message_callback=leilao_finalizado, auto_ack=True)

    channel1.start_consuming()

if __name__ == "__main__":
    try:
        threading.Thread(target=main, daemon=True).start()
        app.run("localhost", port=5002)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
