import pika, time, threading, json, sys, os
from datetime import datetime
from flask import Flask, jsonify, Response, request, make_response

app = Flask(__name__)

leiloes = []

'''
Estrutura JSON do leilão:
{
    "id": int, # Adicionado pelo microserviço
    "nome": str,
    "descricao": str,
    "valor_inicial": float,
    "data_hora_inicio": str,
    "data_hora_fim": str,
    "status": str # Adicionado pelo microserviço
}
'''

@app.route("/auction/create", methods=['POST'])
def create_auction():
    data = request.get_json()
    if all(key in data for key in ("nome", "descricao", "valor_inicial", "data_hora_inicio", "data_hora_fim")):
        data["status"] = "inativo"
        data['id'] = len(leiloes) + 1
        leiloes.append(data)

        with open("logs/leiloes.log", "w") as f:
            json.dump(leiloes, f, indent=4)

        return 'Leilão criado com sucesso', 201
    else:
        return 'Dados incompletos para criação do leilão', 400

@app.route("/auction/consult", methods=['GET'])
def consult_auctions():
    leiloes_ativos = [leilao for leilao in leiloes if leilao["status"] == "ativo"]   
    return jsonify(leiloes_ativos), 200

# ======================================================================================================================================

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=100))
    channel = connection.channel()

    iniciado_queue = channel.queue_declare(queue='', exclusive=True)
    finalizado_queue = channel.queue_declare(queue='', exclusive=True)
    channel.exchange_declare(exchange='leilao', exchange_type='direct')
    channel.queue_bind(exchange='leilao', queue=iniciado_queue.method.queue, routing_key='iniciado')
    channel.queue_bind(exchange='leilao', queue=finalizado_queue.method.queue, routing_key='finalizado')

    while True:
        for leilao in leiloes:
            now = datetime.now()
            inicio = datetime.strptime(leilao['data_hora_inicio'], "%Y-%m-%d %H:%M:%S")
            fim = datetime.strptime(leilao['data_hora_fim'], "%Y-%m-%d %H:%M:%S")
            if leilao["status"] == "inativo" and inicio <= now:
                leilao["status"] = "ativo"
                
                with open("logs/leiloes.log", "w") as f:
                    json.dump(leiloes, f, indent=4)
                
                body = {
                    'id': leilao['id'],
                    'valor_inicial': leilao['valor_inicial'],
                    'status': leilao['status']
                }
                channel.basic_publish(exchange='leilao', routing_key='iniciado', body=str(body))
                print(f" [x] Leilão iniciado: {leilao['descricao']}\n")

            elif leilao["status"] == "ativo" and fim <= now:
                leilao["status"] = "finalizado"

                with open("logs/leiloes.log", "w") as f:
                    json.dump(leiloes, f, indent=4)
                
                body = {
                    'id': leilao['id']
                }
                channel.basic_publish(exchange='leilao', routing_key='finalizado', body=str(body))
                print(f" [x] Leilão finalizado: {leilao['descricao']}\n")

        time.sleep(1)

if __name__ == "__main__":
    try:
        threading.Thread(target=main, daemon=True).start()
        app.run("localhost", port=5001)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)