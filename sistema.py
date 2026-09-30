from flask import Flask, render_template_string, request, redirect, session, jsonify
import os, json
from datetime import datetime

app = Flask(__name__)
app.secret_key = '5d-pro-max-2026'
USER="admin"
PASS="5d"
PIX_KEY="Sofia3x10@gmail.com"

DATA_FILE="data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,'r') as f: return json.load(f)
    return {"produtos":[
        {"id":1,"nome":"Airfryer 4.2L","estoque":12,"compra":200,"venda":350,"img":"🍟"},
        {"id":2,"nome":"TvBox 4K","estoque":20,"compra":80,"venda":150,"img":"📺"},
        {"id":3,"nome":"Cafeteira Elétrica","estoque":8,"compra":90,"venda":189,"img":"☕"},
        {"id":4,"nome":"Forno Elétrico 44L","estoque":5,"compra":300,"venda":499,"img":"🍕"}
    ],"vendas":[],"pedidos":[]}
def save_data(d):
    with open(DATA_FILE,'w') as f: json.dump(d,f)

DASH_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script><title>5D PRO</title></head>
<body class="bg-black text-white"><div class="max-w-7xl mx-auto p-4">
<div class="flex justify-between py-4"><h1 class="text-2xl font-black">5D <span class="text-violet-500">PRO MAX</span></h1>
<div class="flex gap-2"><a href="/loja" target="_blank" class="bg-white text-black px-4 py-2 rounded-full font-bold">Loja</a><a href="/logout" class="bg-zinc-800 px-4 py-2 rounded-full">Sair</a></div></div>
<div class="grid grid-cols-3 gap-3 mb-6">
<div class="bg-zinc-900 p-4 rounded-2xl"><p class="text-zinc-500 text-xs">FATURAMENTO</p><h2 class="text-2xl font-bold">R$ {{faturamento}}</h2></div>
<div class="bg-zinc-900 p-4 rounded-2xl"><p class="text-zinc-500 text-xs">LUCRO</p><h2 class="text-2xl font-bold text-green-400">R$ {{lucro}}</h2></div>
<div class="bg-zinc-900 p-4 rounded-2xl"><p class="text-zinc-500 text-xs">PEDIDOS</p><h2 class="text-2xl font-bold">{{pedidos}}</h2></div>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
{% for p in produtos %}
<div class="bg-zinc-900 border border-zinc-800 p-4 rounded-[24px]"><div class="text-3xl">{{p.img}}</div><h3 class="font-bold">{{p.nome}}</h3><p class="text-xs text-zinc-500">Est: {{p.estoque}}</p><p class="text-xl font-bold">R$ {{p.venda}}</p>
<div class="flex gap-2 mt-3"><form method="POST" action="/vender/{{p.id}}" class="flex-1"><button class="w-full bg-violet-600 py-2 rounded-xl font-bold">VENDER</button></form></div></div>
{% endfor %}</div>
<div class="mt-8"><h3 class="font-bold mb-2">Pedidos da Loja</h3>
{% for v in todos_pedidos[::-1][:20] %}<div class="bg-zinc-900 p-3 rounded-xl mb-2 text-sm"><div class="flex justify-between"><b>{{v.produto}} - R$ {{v.total}}</b><span class="text-green-400">{{v.pagamento}}</span></div><div class="text-zinc-400">{{v.nome}} | {{v.cpf}} | {{v.tel}} | {{v.cep}} - {{v.endereco}}</div><div class="text-zinc-500 text-xs">{{v.data}}</div></div>{% endfor %}</div>
</div></body></html>
"""

LOJA_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script><title>Loja 5D - Oficial</title></head>
<body class="bg-[#f5f5f7]">
<div class="max-w-6xl mx-auto p-4 md:p-6">
<header class="flex justify-between items-center py-4"><h1 class="text-3xl font-black">5D <span class="text-violet-600">STORE</span></h1><div class="bg-black text-white px-4 py-2 rounded-full text-sm">Entrega Express</div></header>
<div class="grid grid-cols-1 md:grid-cols-4 gap-5 mt-6">
{% for p in produtos %}{% if p.estoque>0 %}
<div class="bg-white p-5 rounded-[28px] shadow-sm border border-zinc-100"><div class="bg-zinc-100 h-40 rounded-[20px] flex items-center justify-center text-6xl">{{p.img}}</div>
<h3 class="font-bold mt-4">{{p.nome}}</h3><div class="flex gap-2 items-center"><p class="text-violet-600 font-black text-2xl">R$ {{p.venda}}</p><p class="text-xs line-through text-zinc-400">R$ {{p.venda+80}}</p></div><p class="text-[11px] text-green-600 font-bold">PIX com 5% OFF • Em estoque</p>
<a href="/checkout/{{p.id}}" class="block text-center mt-4 bg-black text-white py-3 rounded-xl font-bold">Comprar Agora</a></div>
{% endif %}{% endfor %}
</div></div>

<div id="robo" class="fixed bottom-5 right-5 z-50"><div id="chat" class="hidden w-80 bg-white rounded-[20px] shadow-2xl border mb-3 overflow-hidden"><div class="bg-black text-white p-4 flex gap-3 items-center"><div class="w-8 h-8 bg-violet-600 rounded-full flex items-center justify-center">🤖</div><div><p class="font-bold text-sm">Suporte 5D</p><p class="text-[10px] text-green-400">● Online agora</p></div></div><div class="p-4 h-64 overflow-y-auto text-sm space-y-3"><div class="bg-zinc-100 p-3 rounded-2xl">Olá! Sou o robô da 5D 🤖 Posso te ajudar com frete, pagamento ou PIX?</div><div class="bg-zinc-100 p-3 rounded-2xl">Temos PIX, Cartão em até 12x, Boleto e calculamos frete por CEP!</div></div><div class="p-3 flex gap-2"><input id="msg" placeholder="Digite..." class="flex-1 bg-zinc-100 rounded-full px-4 py-2 text-sm"><button onclick="send()" class="bg-black text-white px-4 rounded-full">→</button></div></div><button onclick="document.getElementById('chat').classList.toggle('hidden')" class="w-14 h-14 bg-black rounded-full shadow-2xl text-2xl">🤖</button></div>
<script>
function send(){let i=document.getElementById('msg'); if(!i.value)return; let c=document.querySelector('#chat div:nth-child(2)'); c.innerHTML+=`<div class='bg-black text-white p-3 rounded-2xl ml-8'>${i.value}</div>`; setTimeout(()=>{c.innerHTML+=`<div class='bg-zinc-100 p-3 rounded-2xl'>Anotado! Para finalizar, clica em Comprar Agora que já vai com seu PIX Sofia3x10@gmail.com 💜</div>`; c.scrollTop=c.scrollHeight},600); i.value=''}
</script>
</body></html>
"""

CHECKOUT_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script><title>Checkout 5D</title></head>
<body class="bg-zinc-50">
<div class="max-w-5xl mx-auto p-4 grid md:grid-cols-2 gap-6 mt-6">
<div class="bg-white p-6 rounded-[24px] shadow-sm">
<h2 class="text-xl font-black mb-4">Finalizar Compra</h2>
<div class="flex gap-4 items-center bg-zinc-50 p-4 rounded-2xl mb-6"><div class="text-4xl">{{p.img}}</div><div><p class="font-bold">{{p.nome}}</p><p class="text-violet-600 font-black">R$ {{p.venda}}</p></div></div>

<form method="POST" class="space-y-3">
<input name="nome" required placeholder="Nome Completo" class="w-full border p-3.5 rounded-xl">
<div class="grid grid-cols-2 gap-3">
<input name="cpf" id="cpf" required placeholder="CPF" maxlength="14" class="border p-3.5 rounded-xl">
<input name="tel" required placeholder="WhatsApp (11) 9..." class="border p-3.5 rounded-xl">
</div>
<input name="email" type="email" required placeholder="Email para nota fiscal" class="w-full border p-3.5 rounded-xl">
<div class="grid grid-cols-3 gap-3">
<input name="cep" id="cep" required placeholder="CEP" maxlength="9" class="border p-3.5 rounded-xl col-span-1" onblur="buscaCep()">
<input name="endereco" id="end" required placeholder="Rua, número, bairro" class="border p-3.5 rounded-xl col-span-2">
</div>
<p id="frete" class="text-sm text-violet-600 font-bold">Digite o CEP para calcular frete</p>

<h3 class="font-bold mt-6">Forma de Pagamento</h3>
<div class="space-y-2">
<label class="flex items-center gap-3 border-2 border-violet-600 bg-violet-50 p-3 rounded-xl"><input type="radio" name="pag" value="PIX" checked><span class="font-bold">PIX - R$ {{pix_desc}} <span class="text-green-600 text-xs">5% OFF</span></span></label>
<label class="flex items-center gap-3 border p-3 rounded-xl"><input type="radio" name="pag" value="CARTAO"><span>Cartão até 12x</span></label>
<label class="flex items-center gap-3 border p-3 rounded-xl"><input type="radio" name="pag" value="BOLETO"><span>Boleto à vista</span></label>
</div>
<button class="w-full bg-black text-white py-4 rounded-xl font-black mt-4 text-lg">PAGAR AGORA →</button>
</form>
</div>

<div class="bg-black text-white p-6 rounded-[24px] h-fit"><h3 class="font-bold">Resumo</h3><div class="flex justify-between mt-4"><span>{{p.nome}}</span><span>R$ {{p.venda}}</span></div><div class="flex justify-between text-sm text-zinc-400"><span>Frete</span><span id="frete2">a calcular</span></div><hr class="my-4 border-zinc-800"><div class="flex justify-between font-black text-xl"><span>Total</span><span id="total">R$ {{p.venda}}</span></div>
<p class="text-xs text-zinc-500 mt-6">Pagamento seguro via PIX: {{pix}}</p>
</div>
</div>
<script>
function buscaCep(){
let cep=document.getElementById('cep').value.replace(/\\D/g,'');
if(cep.length!=8)return;
fetch(`https://viacep.com.br/ws/${cep}/json/`).then(r=>r.json()).then(d=>{
document.getElementById('end').value=`${d.logradouro}, ${d.bairro} - ${d.localidade}/${d.uf}`;
let frete = d.uf=='SP'? 19.90 : 34.90;
document.getElementById('frete').innerText=`Frete para ${d.localidade}: R$ ${frete} - Entrega 2 a 5 dias`;
document.getElementById('frete2').innerText=`R$ ${frete}`;
document.getElementById('total').innerText=`R$ ${(parseFloat({{p.venda}})+frete).toFixed(2)}`;
});
}
document.getElementById('cpf').addEventListener('input',e=>{let v=e.target.value.replace(/\\D/g,''); v=v.replace(/(\\d{3})(\\d)/,'$1.$2'); v=v.replace(/(\\d{3})(\\d)/,'$1.$2'); v=v.replace(/(\\d{3})(\\d{1,2})$/,'$1-$2'); e.target.value=v});
</script>
</body></html>
"""

PAGO_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-zinc-50 flex items-center justify-center min-h-screen p-4">
<div class="bg-white p-8 rounded-[32px] max-w-md w-full text-center shadow-xl">
<div class="text-6xl mb-4">✅</div><h1 class="text-2xl font-black">Pedido Recebido!</h1><p class="text-zinc-500 mt-2">Pague via PIX para liberar</p>
<div class="bg-zinc-900 text-white p-5 rounded-2xl mt-6 text-left">
<p class="text-xs text-zinc-400">CHAVE PIX (Email)</p><p class="font-mono font-bold text-lg break-all">{{pix}}</p>
<p class="text-xs text-zinc-400 mt-3">VALOR TOTAL</p><p class="font-black text-2xl text-green-400">R$ {{total}}</p>
<p class="text-xs text-zinc-500 mt-2">Envie comprovante no WhatsApp</p>
</div>
<img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={{pix}}" class="mx-auto mt-6 rounded-xl border">
<p class="text-xs text-zinc-400 mt-2">QR Code PIX</p>
<p class="text-sm mt-6 font-bold">{{nome}}, seu pedido {{produto}} foi anotado! Embalaremos após o PIX.</p>
<a href="/loja" class="block mt-6 bg-black text-white py-3 rounded-xl font-bold">Voltar à Loja</a>
</div></body></html>
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

@app.route('/')
def index():
    if not session.get('logado'): return redirect('/login')
    d=load_data()
    fat=sum([v['venda'] for v in d['vendas']]) + sum([p['total'] for p in d.get('pedidos',[])])
    luc=sum([v['lucro'] for v in d['vendas']])
    return render_template_string(DASH_HTML,produtos=d['produtos'],faturamento=fat,lucro=luc,pedidos=len(d.get('pedidos',[])),todos_pedidos=d.get('pedidos',[]))

@app.route('/loja')
def loja():
    d=load_data()
    return render_template_string(LOJA_HTML,produtos=d['produtos'])

@app.route('/checkout/<int:pid>')
def checkout(pid):
    d=load_data()
    prod=next((p for p in d['produtos'] if p['id']==pid),None)
    pix_desc = int(prod['venda']*0.95)
    return render_template_string(CHECKOUT_HTML,p=prod,pix=PIX_KEY,pix_desc=pix_desc)

@app.route('/checkout/<int:pid>',methods=['POST'])
def pagar(pid):
    d=load_data()
    prod=next((p for p in d['produtos'] if p['id']==pid),None)
    if prod and prod['estoque']>0:
        prod['estoque']-=1
        frete = 19.90
        total = prod['venda']+frete
        if request.form.get('pag')=='PIX': total = int(prod['venda']*0.95)+frete
        pedido={"produto":prod['nome'],"total":total,"nome":request.form.get('nome'),"cpf":request.form.get('cpf'),"tel":request.form.get('tel'),"email":request.form.get('email'),"cep":request.form.get('cep'),"endereco":request.form.get('endereco'),"pagamento":request.form.get('pag'),"data":datetime.now().strftime("%d/%m %H:%M")}
        d.setdefault('pedidos',[]).append(pedido)
        save_data(d)
        return render_template_string(PAGO_HTML,pix=PIX_KEY,total=total,nome=pedido['nome'],produto=pedido['produto'])
    return redirect('/loja')

@app.route('/vender/<int:pid>',methods=['POST'])
def vender(pid):
    if not session.get('logado'): return redirect('/login')
    d=load_data()
    for p in d['produtos']:
        if p['id']==pid and p['estoque']>0:
            p['estoque']-=1
            d['vendas'].append({"produto":p['nome'],"venda":p['venda'],"lucro":p['venda']-p['compra'],"data":datetime.now().strftime("%d/%m %H:%M")})
    save_data(d); return redirect('/')

@app.route('/manifest.json')
def manifest():
    return jsonify({"name":"5D STORE","short_name":"5D","start_url":"/loja","display":"standalone","background_color":"#000","theme_color":"#7c3aed"})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
