from flask import Flask, render_template_string, request, redirect, session
import os, json
from datetime import datetime

app = Flask(__name__)
app.secret_key = '5d-ultra-2026'
USER="admin"
PASS="5d"
PIX="Sofia3x10@gmail.com"
MP_LINK="https://www.mercadopago.com.br"
WHATS="5518999999999" # SEU WHATSAPP AQUI
FILE="data.json"

def load():
    if os.path.exists(FILE):
        try:
            with open(FILE,'r') as f: return json.load(f)
        except: pass
    return {"produtos":[
        {"id":1,"nome":"Smart TV 50\" 4K","estoque":6,"compra":400,"venda":560,"img":"https://images.unsplash.com/photo-1593784991095-a205069470b6?w=600"},
        {"id":2,"nome":"Ar-Condicionado 12.000 BTUs","estoque":4,"compra":280,"venda":400,"img":"https://images.unsplash.com/photo-1632851854442-62d8c0d28c7d?w=600"},
        {"id":3,"nome":"Frigobar 120L","estoque":5,"compra":350,"venda":550,"img":"https://images.unsplash.com/photo-1584568821120-7d4c6b0a1ae7?w=600"},
        {"id":4,"nome":"Furadeira Bosch 650W","estoque":15,"compra":60,"venda":99,"img":"https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=600"},
        {"id":5,"nome":"Parafusadeira 12V","estoque":10,"compra":65,"venda":100,"img":"https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=600"},
        {"id":6,"nome":"Airfryer 4.2L","estoque":12,"compra":90,"venda":150,"img":"https://images.unsplash.com/photo-1626147116986-4601771477a9?w=600"},
        {"id":7,"nome":"JBL Boombox 3","estoque":7,"compra":50,"venda":80,"img":"https://images.unsplash.com/photo-1608043152269-423dbba4e7e4?w=600"},
        {"id":8,"nome":"Micro-ondas 30L","estoque":8,"compra":200,"venda":300,"img":"https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=600"},
    ],"pedidos":[]}

def save(d):
    with open(FILE,'w') as f: json.dump(d,f)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        if request.form.get('user')==USER and request.form.get('pass')==PASS:
            session['logado']=True; return redirect('/')
    return '<body style="background:#000;display:flex;justify-content:center;align-items:center;height:100vh"><form method="POST" style="background:#111;padding:32px;border-radius:24px;display:flex;flex-direction:column;gap:12px"><h2 style="color:white;text-align:center">5D</h2><input name="user" placeholder="admin" style="padding:12px;border-radius:12px"><input name="pass" type="password" placeholder="5d" style="padding:12px;border-radius:12px"><button style="background:#7c3aed;color:white;padding:12px;border-radius:12px">ENTRAR</button></form></body>'

@app.route('/logout')
def logout():
    session.clear(); return redirect('/login')

@app.route('/')
def dash():
    if not session.get('logado'): return redirect('/login')
    d=load(); fat=sum([x.get('total',0) for x in d.get('pedidos',[])])
    return render_template_string("""<html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-black text-white p-6"><div class="max-w-6xl mx-auto"><div class="flex justify-between"><h1 class="text-2xl font-black">5D ULTRA</h1><a href="/loja" target="_blank" class="bg-white text-black px-4 py-2 rounded-full font-bold">Ver Loja</a></div><div class="grid grid-cols-2 gap-4 mt-6"><div class="bg-violet-600 p-6 rounded-2xl"><p>FAT</p><h2 class="text-3xl font-bold">R$ {{fat}}</h2></div><div class="bg-zinc-900 p-6 rounded-2xl"><p>PEDIDOS</p><h2 class="text-3xl font-bold">{{ped|length}}</h2></div></div><div class="grid md:grid-cols-4 gap-4 mt-8">{% for p in prods %}<div class="bg-zinc-900 rounded-2xl overflow-hidden"><img src="{{p.img}}" class="h-32 w-full object-cover"><div class="p-3"><h3 class="font-bold text-sm">{{p.nome}}</h3><p>R$ {{p.venda}} - Est {{p.estoque}}</p></div></div>{% endfor %}</div><div class="mt-8 bg-zinc-900 p-6 rounded-2xl">{% for v in ped[::-1] %}<p class="border-b border-zinc-800 py-2 text-sm">{{v.produto}} - {{v.nome}} {{v.tel}} - {{v.pagamento}} R$ {{v.total}}</p>{% endfor %}</div></div></body></html>""",prods=d['produtos'],ped=d.get('pedidos',[]),fat=int(fat))

@app.route('/loja')
def loja():
    d=load()
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-[#fbfbfd]"><div class="max-w-6xl mx-auto p-6">
    <header class="flex justify-between items-center"><h1 class="text-2xl font-black">5D STORE</h1><span class="bg-green-500 text-white px-3 py-1 rounded-full text-xs">Atendimento Online</span></header>
    <h2 class="text-5xl font-black mt-8">Ofertas 5D<br><span class="text-violet-600">Imperdíveis</span></h2>
    <div class="grid md:grid-cols-4 gap-5 mt-8">{% for p in prods %}<div class="bg-white rounded-[24px] p-5 shadow"><img src="{{p.img}}" class="h-44 w-full object-contain bg-zinc-50 rounded-xl"><h3 class="font-bold mt-3 text-sm">{{p.nome}}</h3><p class="text-xl font-black mt-1">R$ {{p.venda}}</p><p class="text-[11px] text-green-600">12x sem juros</p><a href="/checkout/{{p.id}}" class="block bg-black text-white text-center py-3 rounded-full mt-3 font-bold text-sm">Comprar Agora</a></div>{% endfor %}</div>
    </div>
    <!-- ROBÔ WHATSAPP -->
    <div id="robo" style="position:fixed;bottom:20px;right:20px;z-index:9999"><div id="msg" style="background:white;padding:16px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.2);margin-bottom:10px;max-width:260px;font-family:sans-serif;font-size:14px"><b>🤖 Robô 5D:</b> Olá! Vi que gostou do produto. Quer 5% OFF no PIX? Me chama! <span onclick="document.getElementById('msg').style.display='none'" style="float:right;cursor:pointer">x</span></div><a href="https://wa.me/{{whats}}?text=Ola%20quero%20comprar%20na%205D" target="_blank" style="background:#25D366;color:white;width:60px;height:60px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:30px;box-shadow:0 10px 30px rgba(0,0,0,0.3);text-decoration:none">💬</a></div>
    <script>setTimeout(()=>{document.getElementById('msg').style.display='block'},3000)</script>
    </body></html>
    """,prods=d['produtos'],whats=WHATS)

@app.route('/checkout/<int:pid>')
def checkout(pid):
    d=load(); p=next((x for x in d['produtos'] if x['id']==pid),None)
    return render_template_string("""<html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-white"><div class="max-w-4xl mx-auto grid md:grid-cols-2 min-h-screen"><div class="p-8"><h2 class="text-3xl font-black">Checkout Seguro</h2>
    <form method="POST" class="mt-6 space-y-3"><input name="nome" required placeholder="Nome completo" class="w-full border p-4 rounded-2xl"><div class="grid grid-cols-2 gap-2"><input name="cpf" required placeholder="CPF" class="border p-4 rounded-2xl"><input name="tel" required placeholder="WhatsApp" class="border p-4 rounded-2xl"></div><input name="email" required placeholder="Email" class="w-full border p-4 rounded-2xl"><input name="endereco" required placeholder="Endereço + CEP" class="w-full border p-4 rounded-2xl"><div class="pt-4 space-y-2"><label class="flex justify-between border-2 border-violet-600 p-4 rounded-2xl bg-violet-50"><span>PIX - R$ {{pixv}} - {{pix}}</span><input type="radio" name="pag" value="PIX" checked></label><label class="flex justify-between border p-4 rounded-2xl"><span>Cartão / Boleto</span><input type="radio" name="pag" value="CARTAO"></label></div><button class="w-full bg-black text-white py-4 rounded-full font-bold">Pagar R$ {{p.venda}}</button></form></div><div class="bg-zinc-50 p-8"><img src="{{p.img}}" class="rounded-2xl"><h3 class="font-bold text-xl mt-4">{{p.nome}}</h3><p class="text-3xl font-black">R$ {{p.venda}}</p></div></div></body></html>""",p=p,pix=PIX,pixv=int(p['venda']*0.95))

@app.route('/checkout/<int:pid>',methods=['POST'])
def pagar(pid):
    d=load(); p=next((x for x in d['produtos'] if x['id']==pid),None)
    if p and p['estoque']>0:
        p['estoque']-=1; tipo=request.form.get('pag'); total=int(p['venda']*0.95) if tipo=='PIX' else p['venda']
        d.setdefault('pedidos',[]).append({"produto":p['nome'],"total":total,"nome":request.form.get('nome'),"cpf":request.form.get('cpf'),"tel":request.form.get('tel'),"email":request.form.get('email'),"endereco":request.form.get('endereco'),"pagamento":tipo,"data":datetime.now().strftime("%d/%m %H:%M")})
        save(d)
        return render_template_string("""<html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-zinc-100 flex items-center justify-center min-h-screen p-6"><div class="bg-white p-8 rounded-3xl max-w-sm w-full text-center"><div class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center text-white text-2xl mx-auto">✓</div><h1 class="text-2xl font-black mt-4">Pedido Feito!</h1><p class="text-zinc-500">{{msg}}</p><div class="mt-4 bg-black text-white p-4 rounded-2xl"><p>{{pix}}</p><p class="text-xl font-bold text-green-400">R$ {{total}}</p></div><img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={{pix}}" class="mx-auto mt-4 rounded-xl"><a href="/loja" class="block mt-4 bg-black text-white py-3 rounded-full font-bold">Voltar</a></div></body></html>""",pix=PIX,total=total,msg="PIX gerado",tipo=tipo)
    return redirect('/loja')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
