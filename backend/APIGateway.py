import pika, time, sys, os
from flask import Flask, Response, jsonify, request
import requests, threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app, allow_headers=["Content-Type"])

interests = {}
notifications = []

@app.route("/auction/create", methods=['POST'])
def create_auction():
    url = "http://localhost:5001/auction/create"
    response = requests.post(url, json=request.get_json())
    return response.text, response.status_code

@app.route("/auction/consult", methods=['GET'])
def consult_auctions():    
    url = "http://localhost:5001/auction/consult"
    response = requests.get(url)
    return response.json(), response.status_code

@app.route("/bid/make", methods=['POST'])
def make_bid():
    url = "http://localhost:5002/bid/make"
    response = requests.post(url, json=request.get_json())
    return response.text, response.status_code

@app.route("/auction/interest", methods=['POST'])
def set_interest():    
    url = "http://localhost:5001/auction/consult"
    response = requests.get(url)
    if response.status_code == 200:
        leiloes = response.json()
        if leiloes:
            if request.get_json()['id_leilao'] in [leilao['id'] for leilao in leiloes]:
                if request.get_json()['id_user'] not in interests:
                    interests[request.get_json()['id_user']] = []
                interests[request.get_json()['id_user']].append(request.get_json()['id_leilao'])
                response = Response(response="Interesse registrado com sucesso", status=200)

            else:
                response = Response(response="Leilão inexistente", status=404)
        else:
            response = Response(response="Nenhum leilão ativo no momento", status=404)
    else:
        response = Response(response="Erro ao consultar leilões", status=500)
    return response
        
@app.route("/auction/uninterest", methods=['POST'])
def remove_interest():    
    user = request.get_json()['id_user']
    auction_id = request.get_json()['id_leilao']
    if user in interests and auction_id in interests[user]:
        interests[user].remove(auction_id)
        response = Response(response="Interesse removido com sucesso", status=200)
    else:
        response = Response(response="Interesse não encontrado", status=404)
    return response

@app.route('/stream')
def stream():
    channel = request.args.get('channel')
    def event_stream():
        while True:
            for notification in notifications:
                if notification['id_leilao'] in interests.get(channel, []):
                    yield f'data: {notification}\n\n'
            time.sleep(1)
    return Response(event_stream(), content_type='text/event-stream')

def main():
    channel = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=100)).channel()
    lance_validado_queue = channel.queue_declare(queue='', exclusive=True)
    lance_invalidado_queue = channel.queue_declare(queue='', exclusive=True)
    leilao_vencedor_queue = channel.queue_declare(queue='', exclusive=True)
    link_pagamento_queue = channel.queue_declare(queue='', exclusive=True)
    status_pagamento_queue = channel.queue_declare(queue='', exclusive=True)
    channel.exchange_declare(exchange='leilao', exchange_type='direct')
    channel.exchange_declare(exchange='lances', exchange_type='direct')
    channel.exchange_declare(exchange='pagamento', exchange_type='direct')
    channel.queue_bind(exchange='lances', queue=lance_validado_queue.method.queue, routing_key='validado')
    channel.queue_bind(exchange='lances', queue=lance_invalidado_queue.method.queue, routing_key='invalidado')
    channel.queue_bind(exchange='leilao', queue=leilao_vencedor_queue.method.queue, routing_key='vencedor')
    channel.queue_bind(exchange='pagamento', queue=link_pagamento_queue.method.queue, routing_key='link_pagamento')
    channel.queue_bind(exchange='pagamento', queue=status_pagamento_queue.method.queue, routing_key='status_pagamento')

    def callback(ch, method, properties, body):
        notification = {'type': method.routing_key, 'message': body.decode()}
        notifications.append(notification)
        print(f" [x] Notificação recebida: {notification}\n")

    channel.basic_consume(queue=lance_validado_queue.method.queue, on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue=lance_invalidado_queue.method.queue, on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue=leilao_vencedor_queue.method.queue, on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue=link_pagamento_queue.method.queue, on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue=status_pagamento_queue.method.queue, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    try:
        threading.Thread(target=main, daemon=True).start()
        app.run("localhost", port=5000)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
