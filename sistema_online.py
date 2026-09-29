from flask import Flask, request, redirect, session
import os, csv
from flask_cloudflared import run_with_cloudflared

app = Flask(__name__)
app.secret_key = "5d-secret"

ARQ = "nomes.txt"
with open(ARQ, "r") as f:
    nomes = f.read().splitlines()

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form.get("senha") == "5d":
            session["logado"] = True
            return redirect("/")
    return """<body style="background:#000;color:#0f0;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace">
    <form method="post" style="border:1px solid #0f0;padding:30px;text-align:center"><h2>ONLINE - LOGIN</h2><p>Senha: 5d</p>
    <input name="senha" type="password" style="padding:10px"><br><br><button style="padding:10px 30px;background:#0f0">ENTRAR</button></form></body>"""

@app.route("/")
def home():
    if not session.get("logado"): return redirect("/login")
    busca = request.args.get("q","").lower()
    lista = [n for n in nomes if busca in n.lower()] if busca else nomes
    return f"""<body style="font-family:monospace;padding:20px;background:#000;color:#0f0"><h1>🌎 SISTEMA 5D - ONLINE</h1>
    <p>Link público! Mande pra quem quiser.</p>
    <form><input name="q" value="{busca}" style="padding:12px;width:60%;background:#111;color:#0f0;border:1px solid #0f0" placeholder="Buscar..."><button style="padding:12px;background:#0f0">BUSCAR</button></form><br>
    {"".join([f"<div style='padding:10px;border:1px solid #222;margin:5px;background:#0a0a0a'>{n}</div>" for n in lista])}</body>"""

run_with_cloudflared(app)
app.run(port=5000)
