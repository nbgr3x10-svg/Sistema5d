from flask import Flask, render_template_string, request, redirect, session, jsonify
import os, json
from datetime import datetime

app = Flask(__name__)
app.secret_key = '5d-ultra-2026'
USER="admin"
PASS="5d"
PIX="Sofia3x10@gmail.com"

FILE="data.json"
def load():
    if os.path.exists(FILE):
        with open(FILE,'r') as f: return json.load(f)
    return {"produtos":[
        {"id":1,"nome":"Airfryer Philco","estoque":12,"compra":200,"venda":397,"img":"https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500"},
        {"id":2,"nome":"TvBox 4K Stick","estoque":20,"compra":80,"venda":179,"img":"https://images.unsplash.com/photo-1593359677879-a4bb92f367d8?w=500"},
        {"id":3,"nome":"Cafeteira 3 Corações","estoque":8,"compra":90,"venda":219,"img":"https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500"}
    ],"vendas":[],"pedidos":[]}
def save(d): json.dump(d,open(FILE,'w'))

HTML_DASH = """
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script><script src="https://cdn.jsdelivr.net/npm/chart.js"></script></head>
<body class="bg-[#0a0a0a] text-white">
<div class="max-w-[1400px] mx-auto p-6">
<div class="flex justify-between items-center"><h1 class="text-3xl font-black tracking-tight">5D <span class="bg-gradient-to-r from-violet-500 to-fuchsia-500 bg-clip-text text-transparent">ULTRA</span></h1>
<div class="flex gap-2"><a href="/loja" target="_blank" class="bg-white text-black px-6 py-2.5 rounded-full font-bold hover:scale-105 transition">Ver Loja ✨</a><a href="/logout" class="bg-zinc-800 px-4 py-2.5 rounded-full">Sair</a></div></div>

<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mt-8">
<div class="bg-gradient-to-br from-violet-600 to-indigo-600 p-6 rounded-[24px]"><p class="text-violet-200 text-xs">FATURAMENTO</p><h2 class="text-3xl font-black mt-1">R$ {{fat}}</h2><p class="text-xs mt-2 text-violet-200">↑ 12% hoje</p></div>
<div class="bg-zinc-900 border border-zinc-800 p-6 rounded-[24px]"><p class="text-zinc-500 text-xs">LUCRO LÍQUIDO</p><h2 class="text-3xl font-black text-green-400">R$ {{lucro}}</h2></div>
<div class="bg-zinc-900 border border-zinc-800 p-6 rounded-[24px]"><p class="text-zinc-500 text-xs">PEDIDOS</p><h2 class="text-3xl font-black">{{pedidos|length}}</h2></div>
<div class="bg-zinc-900 border border-zinc-800 p-6 rounded-[24px]"><canvas id="c"></canvas></div>
</div>

<div class="grid md:grid-cols-3 gap-6 mt-8">
<div class="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
{% for p in produtos %}
<div class="group bg-zinc-900 border border-zinc-800 rounded-[24px] overflow-hidden hover:border-violet-600 transition">
<img src="{{p.img}}" class="h-40 w-full object-cover group-hover:scale-105 transition">
<div class="p-4"><h3 class="font-bold">{{p.nome}}</h3><p class="text-zinc-500 text-xs">Estoque {{p.estoque}} • Lucro R$ {{p.venda-p.compra}}</p><p class="text-2xl font-black mt-1">R$ {{p.venda}}</p>
<div class="flex gap-2 mt-3"><form method="POST" action="/vender/{{p.id}}" class="flex-1"><button class="w-full bg-white text-black py-2.5 rounded-xl font-bold">Vender</button></form><form method="POST" action="/del/{{p.id}}"><button class="bg-zinc-800 px-4 py-2.5 rounded-xl">🗑</button></form></div></div></div>
{% endfor %}
</div>
<div class="space-y-4">
<div class="bg-zinc-900 border border-zinc-800 p-5 rounded-[24px]">
<h3 class="font-bold mb-3">+ Novo Produto Surpresa</h3>
<form method="POST" action="/add" class="space-y-2">
<input name="nome" required placeholder="Nome" class="w-full bg-black border border-zinc-800 p-3 rounded-xl">
<input name="img" placeholder="Link da foto (opcional)" class="w-full bg-black border border-zinc-800 p-3 rounded-xl text-sm">
<div class="grid grid-cols-2 gap-2"><input name="compra" type="number" required placeholder="Compra" class="bg-black border border-zinc-800 p-3 rounded-xl"><input name="venda" type="number" required placeholder="Venda" class="bg-black border border-zinc-800 p-3 rounded-xl"></div>
<button class="w-full bg-violet-600 py-3 rounded-xl font-bold">Cadastrar Produto</button>
</form>
</div>
<div class="bg-zinc-900 border border-zinc-800 p-5 rounded-[24px]"><h3 class="font-bold mb-2">Pedidos Recentes</h3>
{% for v in pedidos[::-1][:8] %}<div class="py-2 border-b border-zinc-800 text-sm"><b>{{v.produto}}</b> - {{v.nome}}<br><span class="text-zinc-500">{{v.cpf}} • {{v.pagamento}} • R$ {{v.total}}</span></div>{% else %}<p class="text-zinc-500 text-sm">Nenhum pedido ainda</p>{% endfor %}
</div>
</div>
</div>
</div>
<script>new Chart(document.getElementById('c'),{type:'line',data:{labels:['Seg','Ter','Qua','Qui','Hoje'],datasets:[{data:[12,19,8,{{fat//10}},{{fat//8}}],borderColor:'#7c3aed',tension:0.4,fill:true,backgroundColor:'rgba(124,58,237,0.1)'}]},options:{plugins:{legend:{display:false}},scales:{x:{display:false},y:{display:false}}}});</script>
</body></html>
"""

LOJA = """
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-[#fbfbfd] text-zinc-900">
<div class="max-w-[1200px] mx-auto px-6 py-8">
<header class="flex justify-between items-center"><h1 class="text-2xl font-black">5D<span class="text-violet-600">.</span></h1><div class="flex gap-2 text-xs"><span class="bg-black text-white px-3 py-1.5 rounded-full">Frete Grátis SP</span><span class="bg-green-500 text-white px-3 py-1.5 rounded-full">PIX 5% OFF</span></div></header>
<h2 class="text-5xl font-black tracking-tight mt-12">Tecnologia<br>que você <span class="text-violet-600">ama.</span></h2>
<p class="text-zinc-500 mt-3">Entrega em 24h para Buritama e região</p>
<div class="grid md:grid-cols-3 gap-6 mt-10">
{% for p in produtos %}
<div class="bg-white rounded-[32px] p-6 shadow-[0_20px_60px_-20px_rgba(0,0,0,0.15)] hover:shadow-[0_20px_60px_-15px_rgba(124,58,237,0.3)] hover:-translate-y-1 transition">
<img src="{{p.img}}" class="h-56 w-full object-contain rounded-[20px] bg-zinc-50">
<div class="mt-5"><span class="text-[10px] font-bold tracking-widest text-orange-500">NOVO</span><h3 class="font-bold text-xl leading-tight">{{p.nome}}</h3><p class="text-zinc-400 text-xs mt-1">Pronta entrega • {{p.estoque}} unid</p>
<p class="text-2xl font-black mt-3">R$ {{p.venda}}<span class="text-sm font-normal text-zinc-400"> ou 12x de R$ {{(p.venda/12)|int}}</span></p>
<a href="/checkout/{{p.id}}" class="mt-4 block bg-[#0071e3] hover:bg-[#0077ed] text-white text-center py-3.5 rounded-full font-bold">Comprar</a>
<p class="text-center text-[11px] text-zinc-400 mt-2">Entrega grátis • Devolução em 7 dias</p></div></div>
{% endfor %}
</div></div>

<div class="fixed bottom-6 right-6"><button onclick="document.getElementById('bot').classList.toggle('hidden')" class="w-16 h-16 bg-black rounded-full shadow-2xl text-2xl flex items-center justify-center">🤖</button>
<div id="bot" class="hidden absolute bottom-20 right-0 w-80 bg-white rounded-[24px] shadow-2xl border overflow-hidden"><div class="bg-black text-white p-4"><p class="font-bold">Sofia - Suporte 5D</p><p class="text-xs text-zinc-400">Responde em segundos • IA</p></div><div class="p-4 text-sm bg-zinc-50 h-64 overflow-auto">Oi! Sou a Sofia 🤖<br><br>💳 Aceito PIX ({{pix}}), Cartão, Boleto<br>📦 Frete calculado no CEP<br>⚡ Entrega rápida<br><br>Me pergunta qualquer coisa!</div></div></div>
</body></html>
"""

CHECK = """
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-white">
<div class="max-w-5xl mx-auto grid md:grid-cols-2 gap-0 min-h-screen">
<div class="p-8 md:p-12">
<h2 class="text-3xl font-black">Checkout</h2><p class="text-zinc-500 text-sm">Leva 30 segundos</p>
<form method="POST" class="mt-8 space-y-4">
<input name="nome" required placeholder="Nome completo" class="w-full border border-zinc-200 p-4 rounded-2xl">
<div class="grid grid-cols-2 gap-3"><input name="cpf" id="cpf" required placeholder="CPF" class="border border-zinc-200 p-4 rounded-2xl"><input name="tel" required placeholder="WhatsApp" class="border border-zinc-200 p-4 rounded-2xl"></div>
<input name="email" type="email" required placeholder="E-mail" class="w-full border border-zinc-200 p-4 rounded-2xl">
<div class="grid grid-cols-3 gap-3"><input name="cep" id="cep" required placeholder="CEP" onblur="busca()" class="border border-zinc-200 p-4 rounded-2xl"><input id="end" name="endereco" required placeholder="Endereço completo" class="col-span-2 border border-zinc-200 p-4 rounded-2xl"></div>
<p id="frete" class="text-sm font-bold text-violet-600"></p>
<div class="pt-4 space-y-2">
<label class="flex justify-between border-2 border-black p-4 rounded-2xl"><span class="font-bold">PIX com 5% OFF - R$ {{pixv}}</span><input type="radio" name="pag" value="PIX" checked></label>
<label class="flex justify-between border p-4 rounded-2xl"><span>Cartão 12x</span><input type="radio" name="pag" value="CARTAO"></label>
<label class="flex justify-between border p-4 rounded-2xl"><span>Boleto</span><input type="radio" name="pag" value="BOLETO"></label>
</div>
<button class="w-full bg-black text-white py-5 rounded-full font-black text-lg mt-6">Pagar R$ {{p.venda}} →</button>
</form></div>
<div class="bg-zinc-50 p-8 md:p-12"><img src="{{p.img}}" class="rounded-[24px]"><h3 class="font-bold text-xl mt-6">{{p.nome}}</h3><p class="text-3xl font-black mt-2">R$ {{p.venda}}</p><p class="text-sm text-zinc-500 mt-4">PIX: {{pix}}</p></div>
</div>
<script>
function busca(){let c=document.getElementById('cep').value.replace(/\\D/g,''); if(c.length!=8)return; fetch(`https://viacep.com.br/ws/${c}/json/`).then(r=>r.json()).then(d=>{document.getElementById('end').value=`${d.logradouro}, ${d.bairro} - ${d.localidade}`; document.getElementById('frete').innerText=`Frete para ${d.localidade}/${d.uf}: R$ ${(d.uf=='SP'?19.9:34.9)}`})}
document.getElementById('cpf').addEventListener('input',e=>{let v=e.target.value.replace(/\\D/g,''); v=v.replace(/(\\d{3})(\\d)/,'$1.$2'); v=v.replace(/(\\d{3})(\\d)/,'$1.$2'); v=v.replace(/(\\d{3})(\\d{1,2})$/,'$1-$2'); e.target.value=v});
</script>
</body></html>
"""

PAGO = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-[#f5f5f7] flex items-center justify-center min-h-screen p-6"><div class="bg-white p-10 rounded-[40px] max-w-sm w-full text-center shadow-2xl"><div class="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center text-3xl mx-auto">✓</div><h1 class="text-3xl font-black mt-6">Pedido feito!</h1><p class="text-zinc-500 mt-2">Escaneie o PIX abaixo</p><div class="mt-6 bg-zinc-900 text-white p-5 rounded-[20px]"><p class="text-xs text-zinc-400">PIX EMAIL</p><p class="font-mono font-bold">{{pix}}</p><p class="text-2xl font-black text-green-400 mt-2">R$ {{total}}</p></div><img src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={{pix}}&color=000000" class="mx-auto mt-6 rounded-2xl"><a href="/loja" class="block mt-8 bg-black text-white py-4 rounded-full font-bold">Voltar à loja</a><audio autoplay><source src="https://cdn.pixabay.com/audio/2022/03/24/audio_6a9b3d2a6a.mp3" type="audio/mpeg"></audio></div></body></html>"""

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        if request.form.get('user')==USER and request.form.get('pass')==PASS:
            session['logado']=True; return redirect('/')
    return render_template_string('<body style="background:#000;display:flex;justify-content:center;align-items:center;height:100vh"><form method="POST" style="background:#111;padding:32px;border-radius:24px;display:flex;flex-direction:column;gap:12px"><input name="user" placeholder="admin" style="padding:12px;border-radius:12px"><input name="pass" type="password" placeholder="5d" style="padding:12px;border-radius:12px"><button style="background:#7c3aed;color:white;padding:12px;border-radius:12px;font-weight:bold">ENTRAR</button></form></body>')
@app.route('/logout')
def out(): session.clear(); return redirect('/login')
@app.route('/')
def dash():
    if not session.get('logado'): return redirect('/login')
    d=load(); fat=sum([x['venda'] for x in d['vendas']])+sum([x['total'] for x in d.get('pedidos',[])])
    luc=sum([x['venda']-x['compra'] for x in d['produtos'] if False]) + sum([x.get('lucro',0) for x in d['vendas']]) + sum([x['total']*0.3 for x in d.get('pedidos',[])])
    return render_template_string(HTML_DASH,produtos=d['produtos'],fat=int(fat),lucro=int(fat*0.35),pedidos=d.get('pedidos',[]))
@app.route('/loja')
def loja(): return render_template_string(LOJA,produtos=load()['produtos'],pix=PIX)
@app.route('/checkout/<int:pid>')
def check(pid):
    d=load(); p=next((x for x in d['produtos'] if x['id']==pid),None)
    return render_template_string(CHECK,p=p,pix=PIX,pixv=int(p['venda']*0.95))
@app.route('/checkout/<int:pid>',methods=['POST'])
def pay(pid):
    d=load(); p=next((x for x in d['produtos'] if x['id']==pid),None)
    if p and p['estoque']>0:
        p['estoque']-=1
        tot=int(p['venda']*0.95)+19.9 if request.form.get('pag')=='PIX' else p['venda']+19.9
        d.setdefault('pedidos',[]).append({"produto":p['nome'],"total":tot,"nome":request.form.get('nome'),"cpf":request.form.get('cpf'),"tel":request.form.get('tel'),"email":request.form.get('email'),"cep":request.form.get('cep'),"endereco":request.form.get('endereco'),"pagamento":request.form.get('pag'),"data":datetime.now().strftime("%d/%m %H:%M")})
        save(d)
        return render_template_string(PAGO,pix=PIX,total=tot)
    return redirect('/loja')
@app.route('/vender/<int:pid>',methods=['POST'])
def vend(pid):
    if not session.get('logado'): return redirect('/login')
    d=load()
    for p in d['produtos']:
        if p['id']==pid and p['estoque']>0: p['estoque']-=1; d['vendas'].append({"venda":p['venda'],"lucro":p['venda']-p['compra']})
    save(d); return redirect('/')
@app.route('/add',methods=['POST'])
def add():
    d=load(); nid=max([x['id'] for x in d['produtos']],default=0)+1
    d['produtos'].append({"id":nid,"nome":request.form.get('nome'),"estoque":10,"compra":int(request.form.get('compra')), "venda":int(request.form.get('venda')), "img":request.form.get('img') or "https://images.unsplash.com/photo-1525598912003-663126343e1f?w=500"})
    save(d); return redirect('/')
@app.route('/del/<int:pid>',methods=['POST'])
def dele(pid):
    if not session.get('logado'): return redirect('/login')
    d=load(); d['produtos']=[p for p in d['produtos'] if p['id']!=pid]; save(d); return redirect('/')
@app.route('/manifest.json')
def man(): return jsonify({"name":"5D ULTRA","start_url":"/loja","display":"standalone"})

if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
