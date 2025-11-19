import threading
import requests
from ast import literal_eval
import pika
from flask import Flask, request, jsonify
import json, sys, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/payment/notify", methods=['POST'])
def payment_notify():
    data = request.get_json()
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=100))
    channel2 = connection.channel()

    status_pagamento_queue = channel2.queue_declare(queue='', exclusive=True)
    channel2.exchange_declare(exchange='pagamento', exchange_type='direct')
    channel2.queue_bind(exchange='pagamento', queue=status_pagamento_queue.method.queue, routing_key='status_pagamento')

    print(f" [x] Payment status: {data['status']} for auction {data['id_leilao']}\n")
    channel2.basic_publish(exchange='pagamento', routing_key='status_pagamento', body=str({
        "id_leilao": data['id_leilao'],
        "status": data['status'],
        "amount": data['amount'],
        "id_user": data['id_user']
    }))

    print(f" [x] Payment notification received: {data}\n")
    return 'Notification received', 200

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=100))
    channel = connection.channel()
    
    link_pagamento_queue = channel.queue_declare(queue='', exclusive=True)
    vencedor = channel.queue_declare(queue='', exclusive=True)
    channel.exchange_declare(exchange='leilao', exchange_type='direct')
    channel.exchange_declare(exchange='pagamento', exchange_type='direct')
    channel.queue_bind(exchange='pagamento', queue=link_pagamento_queue.method.queue, routing_key='link_pagamento')
    channel.queue_bind(exchange='leilao', queue=vencedor.method.queue, routing_key='vencedor')

    def callback(ch, method, properties, body):
        data = literal_eval(body.decode())
        body = {
            "id_leilao": data['id_leilao'],
            "amount": data['valor_vencedor'],
            "webhook_url": "http://localhost:5003/payment/notify"
        }
        response = requests.post("http://localhost:5004/generate_payment_link", json=body)
        payment_data = response.json()
        if response.status_code == 201:
            print(f" [x] Payment link created for auction {data['id_leilao']}\n")
            channel.basic_publish(exchange='pagamento', routing_key='link_pagamento', body=str({
                "id_leilao": data['id_leilao'],
                "payment_link": payment_data['payment_link'],
                "amount": payment_data['amount'],
                "currency": payment_data['currency']
            }))
        else:
            print(f" [ ] Failed to create payment link for auction {data['id_leilao']}\n")

    channel.basic_consume(queue=vencedor.method.queue, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    try:
        threading.Thread(target=main, daemon=True).start()
        app.run("localhost", port=5003)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
