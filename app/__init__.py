"""
    Init file for DuRoad API
"""
import os
from flask import Flask
# from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import pymysql
# import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv() #load the env file 
from .config import Config #configurations



app = Flask(__name__) 

app.config.from_object(Config)

db = SQLAlchemy(app) #db setup

CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


# csrf = CSRFProtect(app) #csrf token form page and from validation

# Flask-Login login manager
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# api = restful.Api(app, decorators=[csrf.exempt])
# app.config['JWT_COOKIE_CSRF_PROTECT'] = False

from app import views, models
# from app.models import *
