from app import login_manager
from app.models import User
from flask import redirect, url_for, request, jsonify

def get_user(email):
    user = User.query.filter_by(email=email).first()
    if bool(user):
        return user
    return

def authenticate_user(email, password):
    user = get_user(email)
    if user and user.toJSON()["password"] == password:
        return user
    return

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    mimetype = request.accept_mimetypes
    if mimetype['application/json'] >= mimetype['text/html']:
        response = jsonify({'error': 'Acesso não autorizado.'})
        response.status_code = 401
        return response
    return redirect(url_for('controle.index'))