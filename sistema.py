from flask import Flask, render_template_string, request, redirect, session
import os, json
from datetime import datetime

app = Flask(__name__)
app.secret_key = '5d-ultra-2026'
USER="admin"
PASS="5d"
PIX="Sofia3x10@gmail.com"
MP_LINK="https://www.mercadopago.com.br"
FILE="data.json"

def load():
    if os.path.exists(FILE):
        try:
            with open(FILE,'r') as f: 
                return json.load(f)
        except: pass
    return {"produtos":[
        {"id":1,"nome":"Smart TV 50\" 4K TCL","estoque":6,"compra":1400,"venda":2399,"img":"https://images.unsplash.com/photo-1593359677879-a4bb92f367d8?w=600"},
        {"id":2,"nome":"Ar-Condicionado 12.000 BTUs","estoque":4,"compra":1200,"venda":2199,"img":"https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=600"},
        {"id":3,"nome":"Frigobar 120L Brastemp","estoque":5,"compra":800,"venda":1499,"img":"https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=600"},
        {"id":4,"nome":"Furadeira Bosch 650W","estoque":15,"compra":150,"venda":329,"img":"https://images.unsplash.com/photo-1504148455328-c376907d081c?w=600"},
        {"id":5,"nome":"Parafusadeira 12V","estoque":10,"compra":180,"venda":399,"img":"https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?w=600"},
        {"id":6,"nome":"Airfryer Philco 4.2L","estoque":12,"compra":200,"venda":397,"img":"https://images.unsplash.com/photo-1585032226651-759b368d7246?w=600"},
        {"id":7,"nome":"JBL Boombox 3","estoque":7,"compra":600,"venda":1199,"img":"https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600"},
        {"id":8,"nome":"Micro-ondas Electrolux 30L","estoque":8,"compra":350,"venda":699,"img":"https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=600"},
    ],"pedidos":[]}

def save(d):
    with open(FILE,'w') as f:
        json.dump(d,f)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        if request.form.get('user')==USER and request.form.get('pass')==PASS:
            session['logado']=True
            return redirect('/')
    return '<body style="background:#000;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif"><form method="POST" style="background:#111;padding:32px;border-radius:24px;display:flex;flex-direction:column;gap:12px"><h2 style="color:white;text-align:center">5D LOGIN</h2><input name="user" placeholder="admin" style="padding:12px;border-radius:12px"><input name="pass" type="password" placeholder="5d" style="padding:12px;border-radius:12px"><button style="background:#7c3aed;color:white;padding:12px;border-radius:12px;font-weight:bold">ENTRAR</button></form></body>'

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
def dash():
    if not session.get('logado'):
        return redirect('/login')
    d=load()
    fat=sum([x.get('total',0) for x in d.get('pedidos',[])])
    html="""
    <html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-black text-white p-6"><div class="max-w-6xl mx-auto">
    <div class="flex justify-between"><h1 class="text-2xl font-black">5D ULTRA</h1><a href="/loja" target="_blank" class="bg-white text-black px-4 py-2 rounded-full font-bold">Ver Loja</a></div>
    <div class="grid grid-cols-3 gap-4 mt-6"><div class="bg-violet-600 p-6 rounded-2xl"><p>FATURAMENTO</p><h2 class="text-3xl font-bold">R$ {{fat}}</h2></div>
    <div class="bg-zinc-900 p-6 rounded-2xl"><p>PEDIDOS</p><h2 class="text-3xl font-bold">{{ped|length}}</h2></div>
    <div class="bg-zinc-900 p-6 rounded-2xl"><a href="/logout">Sair</a></div></div>
    <div class="grid md:grid-cols-3 gap-4 mt-8">{% for p in prods %}<div class="bg-zinc-900 rounded-2xl overflow-hidden"><img src="{{p.img}}" class="h-40 w-full object-cover"><div class="p-4"><h3 class="font-bold">{{p.nome}}</h3><p>R$ {{p.venda}} - Est {{p.estoque}}</p></div></div>{% endfor %}</div>
    <div class="mt-8 bg-zinc-900 p-6 rounded-2xl"><h3>Pedidos</h3>{% for v in ped[::-1] %}<p class="border-b border-zinc-800 py-2">{{v.produto}} - {{v.nome}} - {{v.pagamento}} R$ {{v.total}}</p>{% endfor %}</div>
    </div></body></html>
    """
    return render_template_string(html,prods=d['produtos'],ped=d.get('pedidos',[]),fat=int(fat))

@app.route('/loja')
def loja():
    d=load()
    html="""
    <html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-zinc-50"><div class="max-w-6xl mx-auto p-6"><h1 class="text-4xl font-black mt-6">5D STORE - 8 Produtos</h1>
    <div class="grid md:grid-cols-3 gap-6 mt-8">{% for p in prods %}<div class="bg-white rounded-3xl p-6 shadow"><img src="{{p.img}}" class="h-56 w-full object-contain bg-zinc-50 rounded-2xl"><h3 class="font-bold mt-4">{{p.nome}}</h3><p class="text-2xl font-black">R$ {{p.venda}}</p><a href="/checkout/{{p.id}}" class="block bg-black text-white text-center py-3 rounded-full mt-3 font-bold">Comprar</a></div>{% endfor %}</div></div></body></html>
    """
    return render_template_string(html,prods=d['produtos'])

@app.route('/checkout/<int:pid>')
def checkout(pid):
    d=load()
    p=next((x for x in d['produtos'] if x['id']==pid),None)
    if not p: return "Produto nao encontrado"
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-white"><div class="max-w-4xl mx-auto grid md:grid-cols-2 min-h-screen"><div class="p-8">
    <h2 class="text-3xl font-black">Checkout</h2>
    <form method="POST" class="mt-6 space-y-3">
    <input name="nome" required placeholder="Nome" class="w-full border p-4 rounded-2xl">
    <div class="grid grid-cols-2 gap-2"><input name="cpf" required placeholder="CPF" class="border p-4 rounded-2xl"><input name="tel" required placeholder="WhatsApp" class="border p-4 rounded-2xl"></div>
    <input name="email" required placeholder="Email" class="w-full border p-4 rounded-2xl">
    <input name="endereco" required placeholder="Endereco completo + CEP" class="w-full border p-4 rounded-2xl">
    <div class="space-y-2 pt-4">
    <label class="flex justify-between border-2 border-violet-600 p-4 rounded-2xl bg-violet-50"><span>PIX - R$ {{pixv}} ({{pix}})</span><input type="radio" name="pag" value="PIX" checked></label>
    <label class="flex justify-between border p-4 rounded-2xl"><span>Cartao / Boleto (Mercado Pago)</span><input type="radio" name="pag" value="MP"></label>
    </div>
    <button class="w-full bg-black text-white py-4 rounded-full font-bold">Finalizar R$ {{p.venda}}</button>
    </form></div><div class="bg-zinc-50 p-8"><img src="{{p.img}}" class="rounded-2xl"><h3 class="font-bold text-xl mt-4">{{p.nome}}</h3><p class="text-2xl font-black">R$ {{p.venda}}</p></div></div>
    <script>document.getElementById('cpf')?.addEventListener('input',e=>{let v=e.target.value.replace(/\\D/g,''); v=v.replace(/(\\d{3})(\\d)/,'$1.$2'); v=v.replace(/(\\d{3})(\\d)/,'$1.$2'); v=v.replace(/(\\d{3})(\\d{1,2})$/,'$1-$2'); e.target.value=v});</script>
    </body></html>
    """,p=p,pix=PIX,pixv=int(p['venda']*0.95))

@app.route('/checkout/<int:pid>',methods=['POST'])
def pagar(pid):
    d=load()
    p=next((x for x in d['produtos'] if x['id']==pid),None)
    if p and p['estoque']>0:
        p['estoque']-=1
        tipo=request.form.get('pag')
        total=int(p['venda']*0.95) if tipo=='PIX' else p['venda']
        d.setdefault('pedidos',[]).append({"produto":p['nome'],"total":total,"nome":request.form.get('nome'),"cpf":request.form.get('cpf'),"tel":request.form.get('tel'),"email":request.form.get('email'),"endereco":request.form.get('endereco'),"pagamento":tipo,"data":datetime.now().strftime("%d/%m %H:%M")})
        save(d)
        return render_template_string("""
        <html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-zinc-100 flex items-center justify-center min-h-screen p-6"><div class="bg-white p-8 rounded-3xl max-w-sm w-full text-center shadow-xl">
        <div class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center text-white text-2xl mx-auto">✓</div>
        <h1 class="text-2xl font-black mt-4">Pedido Feito!</h1><p class="text-zinc-500 mt-2">{{msg}}</p>
        <div class="mt-4 bg-black text-white p-4 rounded-2xl"><p>{{pix}}</p><p class="text-xl font-bold text-green-400">R$ {{total}}</p></div>
        {% if tipo=='PIX' %}<img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={{pix}}" class="mx-auto mt-4">{% else %}<a href="{{mp}}" target="_blank" class="block mt-4 bg-blue-500 text-white py-3 rounded-full font-bold">Pagar Cartao/Boleto</a>{% endif %}
        <a href="/loja" class="block mt-4 bg-zinc-200 py-3 rounded-full font-bold">Voltar Loja</a></div></body></html>
        """,pix=PIX,total=total,tipo=tipo,msg="PIX gerado" if tipo=='PIX' else "Pague seguro no Mercado Pago",mp=MP_LINK)
    return redirect('/loja')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
