from flask import Flask, request, jsonify, render_template_string
import threading

app = Flask(__name__)

# Set para armazenar IPs únicos
ips_visitantes = set()
# Lock para evitar problemas com concorrência
lock = threading.Lock()

# HTML simples com contador ao vivo
HTML = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Notícia Incrível!</title>
    <script>
        async function atualizarContador() {
            const res = await fetch("/contador");
            const data = await res.json();
            document.getElementById("contador").innerText = data.visitas;
        }

        setInterval(atualizarContador, 1000);
        window.onload = atualizarContador;
    </script>
</head>
<body>
    <h1>Notícia Incrível!</h1>
    <p>Essa é uma notícia de teste para contagem de visitas em tempo real.</p>
    <h2>Visitas únicas: <span id="contador">0</span></h2>
</body>
</html>
'''

@app.route("/")
def index():
    # Pega o primeiro IP do header X-Forwarded-For, se existir
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ip = ip.split(",")[0].strip()

    with lock:
        if ip not in ips_visitantes:
            ips_visitantes.add(ip)
    return render_template_string(HTML)

@app.route("/contador")
def contador():
    return jsonify({"visitas": len(ips_visitantes)})
