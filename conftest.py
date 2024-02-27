import pytest
from app import create_app
from app.models import User
from flask_login import login_user, logout_user

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app

@pytest.fixture(scope='function')
def authenticated_user(app, client):
    user = User.query.filter_by(email='teste@teste.com').first()
    with app.test_request_context():
        login_user(user)
        yield user
        logout_user()