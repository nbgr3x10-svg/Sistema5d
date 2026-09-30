from flask import Flask, render_template_string, request, redirect, session, jsonify
import os, json
from datetime import datetime
app=Flask(__name__)
app.secret_key='5d-ultra-2026'
USER="admin"
PASS="5d"
PIX="Sofia3x10@gmail.com"
FILE="data.json"
def load():
    if os.path.exists(FILE):
        with open(FILE,'r') as f: return json.load(f)
    return {"produtos":[
        {"id":1,"nome":"Smart TV 50'' 4K TCL","estoque":6,"compra":1400,"venda":2399,"img":"https://images.unsplash.com/photo-1593359677879-a4bb92f367d8?w=600"},
        {"id":2,"nome":"Ar-Condicionado 12.000 BTUs Inverter","estoque":4,"compra":1200,"venda":2199,"img":"https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=600"},
        {"id":3,"nome":"Frigobar 120L Brastemp","estoque":5,"compra":800,"venda":1499,"img":"https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=600"},
        {"id":4,"nome":"Furadeira Impacto 650W Bosch","estoque":15,"compra":150,"venda":329,"img":"https://images.unsplash.com/photo-1504148455328-c376907d081c?w=600"},
        {"id":5,"nome":"Parafusadeira 12V com Bateria","estoque":10,"compra":180,"venda":399,"img":"https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?w=600"},
        {"id":6,"nome":"Airfryer 4.2L Philco","estoque":12,"compra":200,"venda":397,"img":"https://images.unsplash.com/photo-1585032226651-759b368d7246?w=600"},
        {"id":7,"nome":"Caixa de Som JBL Boombox","estoque":7,"compra":600,"venda":1199,"img":"https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600"},
        {"id":8,"nome":"Micro-ondas 30L Electrolux","estoque":8,"compra":350,"venda":699,"img":"https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=600"},
    ],"vendas":[],"pedidos":[]}
def save(d): json.dump(d,open(FILE,'w'))
# ... (mantém as rotas iguais da versão ULTRA anterior, só trocando a lista de produtos)
