from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from .config import Config

app = Flask(__name__)
db = SQLAlchemy(app)
#csrf = CSRFProtect(app)

# Flask-Login login manager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# api = restful.Api(app, decorators=[csrf.exempt])
# app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config.from_object(Config)
from app import views, models
from app.models import *