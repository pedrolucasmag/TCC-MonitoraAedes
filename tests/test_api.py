from flask import url_for

valid_data = {
    'nome': 'João',
    'email': 'joao@example.com',
    'tel': '123456789',
    'cep': '12515460',
    'rua': 'Rua Anita Garibaldi',
    'numero': 123,
    'bairro': 'Nova Guará',
    'valorvisita': 'manha',
    'valorcontaminacao': ''
}

invalid_ocurrence = b'{"data":{"bairro":["This field is required."]'

def test_add_invalid_occurence_data(client):
    response = client.post(url_for('api.getFormData'), data={'nome':'Maria'})
    assert invalid_ocurrence in response.data


def test_add_valid_occurrence_data(client):
    response = client.post(url_for('api.getFormData'), data=valid_data)
    assert b'{"message":"Formul\\u00e1rio enviado com sucesso!"}\n' in response.data




    