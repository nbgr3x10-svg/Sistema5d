from flask import Flask, render_template_string, request, redirect, session, send_file
import os, json, mercadopago, urllib.parse
from datetime import datetime
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = '5d-ultra-2026'
USER="admin"; PASS="5d"
PIX="Sofia3x10@gmail.com"
TOKEN_MERCADOPAGO="SEU_TOKEN_AQUI"
WHATS="5518999999999"
FILE="data.json"
sdk = mercadopago.SDK(TOKEN_MERCADOPAGO) if "APP_" in TOKEN_MERCADOPAGO else None

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

@app.route('/')
def dash():
    if not session.get('logado'): return redirect('/login')
    d=load()
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-black text-white p-6"><div class="max-w-6xl mx-auto">
    <div class="flex justify-between"><h1 class="font-black text-2xl">5D ULTRA - FAT R$ {{fat}}</h1><div class="flex gap-2"><a href="/loja" class="bg-white text-black px-4 py-2 rounded-full">Loja</a><a href="/logout" class="bg-zinc-800 px-4 py-2 rounded-full">Sair</a></div></div>
    <div class="mt-6 grid gap-2">{% for p in ped[::-1] %}<div class="bg-zinc-900 p-4 rounded-xl flex justify-between items-center"><span>{{p.produto}} - {{p.nome}} - R$ {{p.total}} ({{p.pagamento}}) - {{p.tel}}</span><div class="flex gap-2"><a href="https://wa.me/55{{p.tel}}?text={{ ('Ola '+p.nome+' seu pedido '+p.produto+' de R$ '+p.total|string+' confirmado! Me manda comprovante').replace(' ','%20') }}" target="_blank" class="bg-green-500 px-3 py-1 rounded-full text-xs">Zap</a><a href="/nota/{{p.id_nota}}" class="bg-violet-600 px-3 py-1 rounded-full text-xs">Nota</a></div></div>{% endfor %}</div></div></body></html>
    """,ped=d.get('pedidos',[]),fat=sum([x['total'] for x in d.get('pedidos',[]) ]))

@app.route('/logout')
def logout(): session.clear(); return redirect('/login')

@app.route('/loja')
def loja():
    d=load()
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-[#fbfbfd]">
    <div class="max-w-6xl mx-auto p-6"><h1 class="text-3xl font-black">5D STORE</h1><div class="grid md:grid-cols-4 gap-4 mt-6">
    {% for p in prods %}<div class="bg-white p-4 rounded-2xl shadow"><img src="{{p.img}}" class="h-36 w-full object-contain"><h3 class="font-bold text-sm mt-2">{{p.nome}}</h3><p class="font-black">R$ {{p.venda}} <span class="text-green-600 text-xs">PIX R$ {{(p.venda*0.95)|int}}</span></p><a href="/checkout/{{p.id}}" class="bg-black text-white block text-center py-2 rounded-full mt-2 text-sm">Comprar</a></div>{% endfor %}</div></div>
    <div style="position:fixed;bottom:20px;right:20px"><a href="https://wa.me/{{w}}?text=Quero%20comprar%20com%20desconto" style="background:#25D366;color:white;width:56px;height:56px;display:flex;align-items:center;justify-content:center;border-radius:50%;font-size:28px;text-decoration:none">💬</a></div>
    <script>let a=false; setTimeout(()=>{if(!a){a=true; if(confirm('🤖 5D: Te dou 5% OFF no PIX se fechar agora. Quer?')){window.location.href='/checkout/1'}}},8000)</script>
    </body></html>""",prods=d['produtos'],w=WHATS)

@app.route('/checkout/<int:pid>')
def checkout(pid):
    d=load(); p=next((x for x in d['produtos'] if x['id']==pid),None)
    return render_template_string("""<html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-white"><div class="max-w-3xl mx-auto p-6"><h2 class="text-3xl font-black">Finalizar {{p.nome}}</h2><form method="POST" class="mt-6 space-y-3"><input name="nome" required placeholder="Nome completo" class="w-full border p-4 rounded-xl"><input name="cpf" required placeholder="CPF" class="w-full border p-4 rounded-xl"><input name="tel" required placeholder="WhatsApp com DDD ex: 18999999999" class="w-full border p-4 rounded-xl"><select name="pag" class="w-full border p-4 rounded-xl"><option value="PIX">PIX 5% OFF R$ {{pixv}}</option><option value="CARTAO">Cartão até 12x R$ {{p.venda}}</option></select><button class="w-full bg-violet-600 text-white py-4 rounded-full font-bold">GERAR PAGAMENTO + NOTA</button></form></div></body></html>""",p=p,pixv=int(p['venda']*0.95))

@app.route('/checkout/<int:pid>',methods=['POST'])
def pagar(pid):
    d=load(); p=next((x for x in d['produtos'] if x['id']==pid),None)
    nome=request.form.get('nome'); tel=request.form.get('tel'); pag=request.form.get('pag'); total=int(p['venda']*0.95) if pag=='PIX' else p['venda']
    id_nota=datetime.now().strftime("%Y%m%d%H%M%S")
    link_mp = ""
    if sdk:
        try:
            pref = sdk.preference().create({"items":[{"title":p['nome'],"quantity":1,"unit_price":float(total)}],"back_urls":{"success":"https://sistema5d.onrender.com/loja"}})
            link_mp = pref["response"].get("init_point","")
        except: pass
    d.setdefault('pedidos',[]).append({"id_nota":id_nota,"produto":p['nome'],"total":total,"nome":nome,"cpf":request.form.get('cpf'),"tel":tel,"pagamento":pag,"data":datetime.now().strftime("%d/%m/%Y"),"link_mp":link_mp})
    if p: p['estoque']-=1
    save(d)
    wa_cliente = urllib.parse.quote(f"Olá {nome}! Seu pedido da 5D {p['nome']} R$ {total} gerado. Chave PIX: {PIX}. Me manda comprovante aqui!")
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width"><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-zinc-50 flex justify-center p-6"><div class="bg-white p-8 rounded-3xl max-w-md w-full text-center">
    <h1 class="text-2xl font-black">Pedido Gerado!</h1>
    {% if pag=='PIX' %}<p class="mt-2">Pague via PIX</p><div class="bg-black text-white p-3 rounded-xl mt-3 text-sm break-all">{{pix}}</div><p class="font-bold text-xl mt-2">R$ {{total}}</p><img src="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={{pix}}" class="mx-auto mt-3">{% else %}
    {% if link %}<a href="{{link}}" target="_blank" class="block bg-violet-600 text-white py-4 rounded-full mt-4 font-bold">PAGAR COM CARTÃO AGORA</a>{% else %}<p class="mt-4 text-sm">Cartão offline - chama no zap</p>{% endif %}{% endif %}
    <a href="https://wa.me/55{{tel}}?text={{wa}}" target="_blank" class="block bg-green-500 text-white py-3 rounded-full mt-3 font-bold">ENVIAR COBRANÇA NO WHATS DO CLIENTE</a>
    <a href="/nota/{{id}}" class="block border py-3 rounded-full mt-3 font-bold">Baixar Nota Fiscal PDF</a><a href="/loja" class="block mt-2 text-sm">Voltar</a></div></body></html>
    """,pix=PIX,total=total,pag=pag,link=link_mp,id=id_nota,tel=tel,wa=wa_cliente)

@app.route('/nota/<id>')
def nota(id):
    d=load(); ped=next((x for x in d['pedidos'] if x['id_nota']==id),None)
    if not ped: return "Nota não encontrada"
    pdf=FPDF(); pdf.add_page(); pdf.set_font("Arial","B",16); pdf.cell(0,10,"NOTA FISCAL - 5D STORE",ln=True,align='C'); pdf.ln(10)
    pdf.set_font("Arial","",12); pdf.cell(0,8,f"Nota: {ped['id_nota']}",ln=True); pdf.cell(0,8,f"Data: {ped['data']}",ln=True); pdf.cell(0,8,f"Cliente: {ped['nome']} CPF: {ped['cpf']} Tel: {ped['tel']}",ln=True); pdf.cell(0,8,f"Produto: {ped['produto']}",ln=True); pdf.cell(0,8,f"Total: R$ {ped['total']} - {ped['pagamento']}",ln=True)
    pdf.ln(10); pdf.cell(0,8,"Obrigado pela compra! Garantia 90 dias.",ln=True,align='C')
    path=f"/tmp/nota_{id}.pdf"; pdf.output(path); return send_file(path,as_attachment=True)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
