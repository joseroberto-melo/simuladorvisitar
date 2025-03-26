from flask import Flask
import os
import requests

app = Flask(__name__)

WEBHOOK_URL = 'https://discord.com/api/webhooks/...'  # sua webhook aqui
ARQUIVO_CONTADOR = "contador.txt"
emoji_amarelo = "🔶"
emoji_preto = "⚫"

def enviar_mensagem():
    if not os.path.exists(ARQUIVO_CONTADOR):
        with open(ARQUIVO_CONTADOR, "w") as f:
            f.write("2")

    with open(ARQUIVO_CONTADOR, "r") as f:
        dia_atual = int(f.read().strip()) + 1

    with open(ARQUIVO_CONTADOR, "w") as f:
        f.write(str(dia_atual))

    if dia_atual % 2 == 1:
        mensagem = f"{emoji_amarelo}{emoji_preto} Dia {dia_atual} sem Gol de Placa!"
    else:
        mensagem = f"{emoji_amarelo}{emoji_preto} Dia {dia_atual} sem Gol de Placa."

    data = {"content": mensagem}
    response = requests.post(WEBHOOK_URL, json=data)

    print("Mensagem enviada!" if response.status_code == 204 else f"Erro: {response.status_code}")

@app.route('/')
def home():
    return "Servidor do Gol de Placa está ativo!"

@app.route('/disparar')
def disparar():
    enviar_mensagem()
    return "Mensagem enviada pro Discord!"
