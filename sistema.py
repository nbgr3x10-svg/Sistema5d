from flask import Flask, request, redirect, session, jsonify, Response
import os, csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = "5d-secret-pro-max"

ARQ = "nomes.txt"
if os.path.exists(ARQ):
    with open(ARQ, "r") as f:
        nomes = f.read().splitlines()
else:
    nomes = ["Nbgrrec3x10", "hariel", "atalia"]

buscas = 0

def salvar():
    with open(ARQ, "w") as f:
        for n in nomes:
            f.write(n + "\n")

@app.route("/manifest.json")
def manifest():
    return jsonify({
        "name": "Sistema 5D PRO",
        "short_name": "5D PRO",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#000000",
        "theme_color": "#00ff88",
        "icons": [
            {"src": "https://cdn-icons-png.flaticon.com/512/2103/2103633.png", "sizes": "512x512", "type": "image/png"}
        ]
    })

@app.route("/sw.js")
def sw():
    js = """
    self.addEventListener('install', e => self.skipWaiting());
    self.addEventListener('activate', e => self.clients.claim());
    """
    return Response(js, mimetype='application/javascript')

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "5d":
        if request.form.get("senha") == "5d":
            session["logado"] = True
            return redirect("/")
    return """
    <head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#00ff88">
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2103/2103633.png">
    </head>
    <body style="background:#000;color:#0f0;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace">
    <form method="post" style="border:1px solid #0f0;padding:30px;text-align:center;border-radius:10px">
        <h2>⚡ SISTEMA 5D PRO</h2><p>Senha: 5d</p>
        <input name="senha" type="password" placeholder="Senha" style="padding:12px;width:80%"><br><br>
        <button style="padding:12px 30px;background:#0f0;color:#000;font-weight:bold;border:none;border-radius:5px">ENTRAR</button>
    </form>
    <script>navigator.serviceWorker&&navigator.serviceWorker.register('/sw.js')</script>
    </body>
    """

@app.route("/")
def home():
    global buscas
    if not session.get("logado"):
        return redirect("/login")
    busca = request.args.get("q", "").lower()
    if busca:
        buscas += 1
    lista = [n for n in nomes if busca in n.lower()] if busca else nomes

    return f"""
    <head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#00ff88">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2103/2103633.png">
    <title>Sistema 5D PRO</title>
    </head>
    <body style="font-family:monospace; padding:15px; background:#000; color:#00ff88; max-width:600px; margin:auto">
    <h1>⚡ SISTEMA 5D v5 PRO <small style="font-size:12px;color:#555">APP</small></h1>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
        <div style="border:1px solid #0f0;padding:8px 12px;border-radius:5px">Total: {len(nomes)}</div>
        <div style="border:1px solid #0f0;padding:8px 12px;border-radius:5px">Buscas: {buscas}</div>
        <div style="border:1px solid #0f0;padding:8px 12px;border-radius:5px">{datetime.now().strftime('%H:%M:%S')}</div>
    </div><br>
    <form>
        <input name="q" value="{busca}" placeholder="Buscar..." style="padding:12px; width:60%; background:#111; color:#0f0; border:1px solid #0f0; border-radius:5px">
        <button style="padding:12px; background:#0f0; color:#000; border:none; border-radius:5px">BUSCAR</button>
        <a href="/export" style="padding:12px; background:#111; color:#0f0; border:1px solid #0f0; text-decoration:none; border-radius:5px">CSV</a>
    </form><br>
    <form action="/add" method="post">
        <input name="nome" placeholder="Novo nome" style="padding:12px; width:60%; background:#111; color:#0f0; border:1px solid #0f0; border-radius:5px">
        <button style="padding:12px; background:#00ff88; color:#000; font-weight:bold; border:none; border-radius:5px">+ ADD</button>
    </form><hr style="border-color:#0f02a">
    <p style="color:#555;font-size:12px">Toque em "Instalar" no menu do Chrome para virar APK</p>
    {"".join([f"<div style='padding:12px; border:1px solid #222; margin:6px 0; background:#0a0a0a; border-radius:8px'> <b>{i+1:02d}</b> - {n} <a href='/del/{nomes.index(n)}' style='color:#f00; float:right; text-decoration:none'>[X]</a></div>" for i,n in enumerate(lista)])}
    <br><a href="/login" style="color:#555">Sair</a>
    <script>navigator.serviceWorker&&navigator.serviceWorker.register('/sw.js')</script>
    </body>
    """

@app.route("/add", methods=["POST"])
def add():
    novo = request.form.get("nome","").strip()
    if novo:
        nomes.append(novo)
        salvar()
    return redirect("/")

@app.route("/del/<int:idx>")
def delete(idx):
    if 0 <= idx < len(nomes):
        nomes.pop(idx)
        salvar()
    return redirect("/")

@app.route("/export")
def export():
    with open("nomes.csv","w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["id","nome"])
        for i,n in enumerate(nomes):
            w.writerow([i+1,n])
    return redirect("/")

if __name__ == "__main__":
    print("PRO rodando em http://127.0.0.1:5000 - Senha: 5d")
    app.run(host="0.0.0.0", port=5000)
