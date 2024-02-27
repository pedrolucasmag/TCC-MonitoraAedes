from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user
from app.controllers.handleOccurrences import get_occurrences_bairros
import datetime
import os


controle = Blueprint(
    'controle', __name__,
    url_prefix='/controle',
    template_folder='templates',
    static_folder='static'
)

@controle.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('controle.dashboard'))
    return render_template('login.html')


@controle.route('/dashboard')
@login_required
def dashboard():
    ano = datetime.datetime.now().year
    municipio = os.environ.get('MUNICIPIO')
    bairros = get_occurrences_bairros()
    return render_template('dashboard.html', user=current_user,municipio=municipio,ano=ano,bairros=bairros)


@controle.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('controle.index'))