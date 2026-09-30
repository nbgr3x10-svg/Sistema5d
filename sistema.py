from flask import Flask, render_template_string, request, redirect, session, jsonify
import os, json
from datetime import datetime

app = Flask(__name__)
app.secret_key = '5d-pro-max-2026'
USER="admin"
PASS="5d"

DATA_FILE="data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,'r') as f: return json.load(f)
    return {"produtos":[
        {"id":1,"nome":"Airfryer","estoque":12,"compra":200,"venda":350},
        {"id":2,"nome":"TvBox","estoque":20,"compra":80,"venda":150},
        {"id":3,"nome":"Cafeteira","estoque":8,"compra":90,"venda":189},
        {"id":4,"nome":"Forno Elétrico","estoque":5,"compra":300,"venda":499}
    ],"vendas":[]}
def save_data(d):
    with open(DATA_FILE,'w') as f: json.dump(d,f)

BASE_CSS = "https://cdn.tailwindcss.com"
# --- HTMLS ---
DASH_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script><link rel="manifest" href="/manifest.json"><title>5D PRO</title></head>
<body class="bg-black text-white">
<div class="max-w-7xl mx-auto p-4">
<div class="flex justify-between items-center py-4"><h1 class="text-2xl font-black">5D <span class="text-violet-500">PRO MAX</span></h1>
<div class="flex gap-2"><a href="/loja" target="_blank" class="bg-white text-black px-4 py-2 rounded-full font-bold">Ver Loja</a><a href="/logout" class="bg-zinc-800 px-4 py-2 rounded-full">Sair</a></div></div>

<div class="grid grid-cols-3 gap-3 mb-6">
<div class="bg-zinc-900 p-4 rounded-2xl"><p class="text-zinc-500 text-xs">FATURAMENTO</p><h2 class="text-2xl font-bold">R$ {{faturamento}}</h2></div>
<div class="bg-zinc-900 p-4 rounded-2xl"><p class="text-zinc-500 text-xs">LUCRO</p><h2 class="text-2xl font-bold text-green-400">R$ {{lucro}}</h2></div>
<div class="bg-zinc-900 p-4 rounded-2xl"><p class="text-zinc-500 text-xs">VENDAS</p><h2 class="text-2xl font-bold">{{total_vendas}}</h2></div>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
{% for p in produtos %}
<div class="bg-zinc-900 border border-zinc-800 p-4 rounded-[24px]">
<h3 class="font-bold text-lg">{{p.nome}}</h3>
<p class="text-xs text-zinc-500">Estoque: {{p.estoque}} | Lucro: R$ {{p.venda-p.compra}}</p>
<p class="text-xl font-bold mt-2">R$ {{p.venda}}</p>
<div class="flex gap-2 mt-3">
<form method="POST" action="/vender/{{p.id}}" class="flex-1"><button class="w-full bg-violet-600 py-2.5 rounded-xl font-bold">VENDER</button></form>
<form method="POST" action="/del/{{p.id}}"><button class="bg-zinc-800 px-3 py-2.5 rounded-xl">X</button></form>
</div>
</div>
{% endfor %}
</div>

<form method="POST" action="/add" class="mt-8 bg-zinc-900 p-4 rounded-2xl grid grid-cols-2 md:grid-cols-5 gap-2">
<input name="nome" placeholder="Produto" required class="bg-black border border-zinc-800 p-3 rounded-xl col-span-2">
<input name="compra" type="number" placeholder="Compra" required class="bg-black border border-zinc-800 p-3 rounded-xl">
<input name="venda" type="number" placeholder="Venda" required class="bg-black border border-zinc-800 p-3 rounded-xl">
<button class="bg-white text-black font-bold rounded-xl">+ Add</button>
</form>

<div class="mt-8"><h3 class="font-bold mb-2">Últimas Vendas</h3>{% for v in vendas[::-1][:10] %}<div class="text-sm text-zinc-400 flex justify-between border-b border-zinc-900 py-2"><span>{{v.data}} - {{v.produto}}</span><span class="text-green-400">+R$ {{v.lucro}}</span></div>{% endfor %}</div>
</div></body></html>
"""

LOJA_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script><title>Loja 5D</title></head>
<body class="bg-zinc-50">
<div class="max-w-6xl mx-auto p-6"><h1 class="text-4xl font-black mb-2">LOJA <span class="text-violet-600">5D</span></h1><p class="text-zinc-500 mb-8">Entrega para todo Brasil</p>
<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
{% for p in produtos %}{% if p.estoque>0 %}
<div class="bg-white p-4 rounded-[24px] shadow-sm"><div class="bg-zinc-100 h-32 rounded-2xl mb-3 flex items-center justify-center text-3xl">📦</div>
<h3 class="font-bold">{{p.nome}}</h3><p class="text-violet-600 font-black text-xl">R$ {{p.venda}}</p><p class="text-xs text-zinc-400">12x no cartão</p>
<a href="https://wa.me/55SEUNUMERO?text=Quero {{p.nome}}" class="block text-center mt-3 bg-black text-white py-2.5 rounded-xl font-bold">Comprar no Zap</a>
</div>{% endif %}{% endfor %}
</div></div></body></html>
"""

LOGIN_HTML="""<!DOCTYPE html><html><head><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-black flex items-center justify-center h-screen">
<form method="POST" class="bg-zinc-900 p-8 rounded-[24px] w-80 border border-zinc-800">
<h2 class="text-white text-2xl font-black mb-6 text-center">5D PRO</h2>
<input name="user" placeholder="Usuário" class="w-full bg-black border border-zinc-800 text-white p-3 rounded-xl mb-3">
<input name="pass" type="password" placeholder="Senha" class="w-full bg-black border border-zinc-800 text-white p-3 rounded-xl mb-4">
<button class="w-full bg-violet-600 py-3 rounded-xl text-white font-bold">ENTRAR</button>
{% if erro %}<p class="text-red-400 text-sm mt-3 text-center">{{ erro }}</p>{% endif %}
</form></body></html>"""

@app.route('/login',methods=['GET','POST'])
def login():
    erro=None
    if request.method=='POST':
        if request.form.get('user')==USER and request.form.get('pass')==PASS:
            session['logado']=True
            return redirect('/')
        erro="Errado"
    return render_template_string(LOGIN_HTML,erro=erro)
@app.route('/logout')
def logout():
    session.clear(); return redirect('/login')
@app.before_request
def chk():
    if request.path not in ['/login','/loja','/manifest.json'] and not request.path.startswith('/static'):
        if not session.get('logado') and not request.path.startswith('/loja'):
            if request.path not in ['/login']:
                if '/loja' not in request.path:
                    pass
        if request.path in ['/','/add'] or request.path.startswith('/vender') or request.path.startswith('/del'):
            if not session.get('logado'): return redirect('/login')

@app.route('/')
def index():
    d=load_data()
    fat=sum([v['venda'] for v in d['vendas']])
    luc=sum([v['lucro'] for v in d['vendas']])
    return render_template_string(DASH_HTML,produtos=d['produtos'],vendas=d['vendas'],faturamento=fat,lucro=luc,total_vendas=len(d['vendas']))

@app.route('/loja')
def loja():
    d=load_data()
    return render_template_string(LOJA_HTML,produtos=d['produtos'])

@app.route('/add',methods=['POST'])
def add():
    d=load_data()
    nid=max([p['id'] for p in d['produtos']],default=0)+1
    d['produtos'].append({"id":nid,"nome":request.form.get('nome'),"estoque":10,"compra":int(request.form.get('compra')), "venda":int(request.form.get('venda'))})
    save_data(d); return redirect('/')

@app.route('/vender/<int:pid>',methods=['POST'])
def vender(pid):
    d=load_data()
    for p in d['produtos']:
        if p['id']==pid and p['estoque']>0:
            p['estoque']-=1
            d['vendas'].append({"produto":p['nome'],"venda":p['venda'],"lucro":p['venda']-p['compra'],"data":datetime.now().strftime("%d/%m %H:%M")})
    save_data(d); return redirect('/')

@app.route('/del/<int:pid>',methods=['POST'])
def delete(pid):
    d=load_data()
    d['produtos']=[p for p in d['produtos'] if p['id']!=pid]
    save_data(d); return redirect('/')

@app.route('/manifest.json')
def manifest():
    return jsonify({"name":"5D PRO MAX","short_name":"5D PRO","start_url":"/","display":"standalone","background_color":"#000","theme_color":"#7c3aed"})

if __name__=='__main__':
    port=int(os.environ.get("PORT",10000))
    app.run(host='0.0.0.0',port=port)
