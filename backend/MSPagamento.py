import threading
import requests
from ast import literal_eval
import pika
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/payment/notify", methods=['POST'])
def payment_notify():
    data = request.get_json()
    print(f" [x] Payment notification received: {data}\n")
    return 'Notification received', 200

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=100))
    channel = connection.channel()

    vencedor = channel.queue_declare(queue='', exclusive=True)
    channel.exchange_declare(exchange='leilao', exchange_type='direct')
    channel.queue_bind(exchange='leilao', queue=vencedor.method.queue, routing_key='vencedor')

    def callback(ch, method, properties, body):
        data = literal_eval(body.decode())

        body = json.dumps(
            {
            "amount": data['valor_vencedor'],
            "custom_code": "YOURAPPCODE",
            "notification_url": "https://your.endpoint.to.update",
            "beneficiary": {
                "name": "The Name",
                "bank_code": "147",
                "bank_branch": "0000",
                "bank_branch_digit": "1",
                "account": "1030000",
                "account_digit": "1",
                "account_type": "CHECKING",
                "document": "12533009091",
                "document_type": "cpf",
                "pix_key": "userpixkey@user.com",
                "city": "Curitiba",
                "province_code": "PR",
                "address": "Rua a Número 10"
                },
            "legal_entity_name": "Your client's name",
            "website": "Your client's website",
            "merchant_id": 27683029.04591699,
            "source_currency": "USD"
            }
        )
        response = requests.post("https://api.wepayout.com.br/v1/payout/payments", json=body)
        if response.status_code == 201:
            print(f" [x] Payment link created for auction {data['id_leilao']}: {response.json()}\n")
        else:
            print(f" [ ] Failed to create payment link for auction {data['id_leilao']}\n")

    channel.basic_consume(queue=vencedor.method.queue, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    threading.Thread(target=main, daemon=True).start()
    app.run("localhost", port=5003)