import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from flask_marshmallow import Marshmallow
from flask_minify import Minify
from flask_cors import CORS
import flask_login

load_dotenv('.env')

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
ma = Marshmallow()
login_manager = flask_login.LoginManager()
minify = Minify()
cors = CORS()

def create_app():
    app = Flask(__name__, static_folder=None)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

    if 'DYNO' in os.environ:
        Talisman(app, content_security_policy=None)

    csrf.init_app(app)
    
    from app.models import User, Occurrences

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)
    minify.init_app(app)

    from app.views.public.routes import public
    from app.views.controle.routes import controle
    from app.views.api.routes import api

    app.register_blueprint(public)
    app.register_blueprint(controle)
    app.register_blueprint(api)
    

    return app
