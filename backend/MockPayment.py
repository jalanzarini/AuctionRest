from flask import Flask, Response, request, jsonify
import json, requests, sys, os

app = Flask(__name__)

leiloes = []

@app.route("/generate_payment_link", methods=['POST'])
def generate_payment_link():
    """
    Recebe uma requisição para gerar um link de pagamento simulado.
    Espera um JSON com os campos: id_leilao, amount, webhook_url.
    Retorna um link de pagamento simulado ou mensagem de erro.
    """
    data = request.get_json()
    if all(key in data for key in ("id_leilao", "amount", "webhook_url")):
        print(f" [x] Payment link generation request received: {data}\n")
        response = {
            "payment_link": f"http://localhost:5004/mockpayment/{data['id_leilao']}",
            "amount": data['amount'],
            "currency": "BRL"
        }
        leiloes.append({"id_leilao": data['id_leilao'], "amount": data['amount'], "webhook_url": data['webhook_url']})
        return jsonify(response), 201
    else:
        return 'Dados incompletos para geração do link de pagamento', 400

@app.route("/mockpayment/<int:id_leilao>", methods=['POST'])
def mock_payment(id_leilao):
    """
    Simula pagamento sendo realizado.
    Espera JSON com campo: amount.
    Notifica webhook com status do pagamento (sucesso ou fracasso).
    """
    data = request.get_json()

    webhook_url = next((leilao["webhook_url"] for leilao in leiloes if leilao["id_leilao"] == int(id_leilao)), None)
    amount = next((leilao['amount'] for leilao in leiloes if leilao["id_leilao"] == int(id_leilao)), None)

    print(f" [x] Mock payment received: {data}\n")
    if all(key in data for key in ("id_user", "amount")):
        if data['amount'] >= amount:
            text = 'Pagamento realizado com sucesso'
            status = 200
            body = {
                "id_leilao": id_leilao,
                "amount": data['amount'],
                "id_user": data['id_user'],
                "status": "success"
            }
        else:
            text = 'Pagamento falhou: valor insuficiente'
            status = 400
            body = {
                "id_leilao": id_leilao,
                "amount": data['amount'],
                "id_user": data['id_user'],
                "status": "failure"
            }
    if webhook_url:
        requests.post(webhook_url, json=body)
    return text, status
            

if __name__ == "__main__":
    try:
        app.run("localhost", port=5004)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)