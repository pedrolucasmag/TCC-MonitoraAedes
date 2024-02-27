from flask import url_for
import re

def test_index_page(client):
    response = client.get(url_for('controle.index'))
    assert response.status_code == 200
    assert b"Acesso ao sistema de monitoria" in response.data

def test_dashboard_page_without_login(client):
    response = client.get(url_for('controle.dashboard'))
    assert response.status_code == 401
    assert b'{"error":"Acesso n\\u00e3o autorizado."}\n'

def test_dashboard_autenticated(client):
    response = client.get(url_for('controle.index'))
    csrf_token = re.search(r'name="csrf_token"\s+value="([^"]+)"', response.data.decode()).group(1)
    response = client.post(url_for('api.autenticarUsuario'), 
                            data={'email': 'teste@teste.com', 'password': 'teste123', 'csrf_token': csrf_token})
    assert b'{"data":{"messsage":"Usu\\u00e1rio autenticado com sucesso."}}\n' in response.data