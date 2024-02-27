from flask import Blueprint, render_template, json
from pathlib import Path
import os

public = Blueprint(
    'public', __name__,
    template_folder='templates',
    static_folder='static'
)

@public.route('/')
def home():
    municipio = os.getenv("MUNICIPIO")
    return render_template('index.html',municipio=municipio)

@public.route('/sucesso')
def sucesso():
    return render_template('formSucesso.html')

@public.route('/doencas')
def doencas():
    data = Path(public.static_folder) / 'json' / 'doencas.json'
    doencas = json.load(open(data,encoding='utf-8'))
    return render_template('doencas.html',doencas=doencas)

@public.route('/prevencao')
def prevencao():
    data = Path(public.static_folder) / 'json' / 'dicasPrevencao.json'
    dicas_prevencao = json.load(open(data,encoding='utf-8'))
    return render_template('prevencao.html',dicas_prevencao=dicas_prevencao)