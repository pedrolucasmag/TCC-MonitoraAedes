from flask import url_for

header = b'<h1 class="text-center pt-2">MonitoraAedes</h1>'
sucesso = 'Seu formulário foi recebido com sucesso!'

def test_home_page(client):
    response = client.get(url_for('public.home'))
    assert response.status_code == 200
    assert b'MonitoraAedes' in response.data

def test_success_page(client):
    response = client.get(url_for('public.sucesso'))
    assert response.status_code == 200
    assert sucesso in response.data.decode('utf-8')

def test_diseases_page(client):
    response = client.get(url_for('public.doencas'))
    assert response.status_code == 200
    assert header in response.data

def test_prevention_page(client):
    response = client.get(url_for('public.prevencao'))
    assert response.status_code == 200
    assert header in response.data