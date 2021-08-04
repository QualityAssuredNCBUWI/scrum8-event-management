import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import pymysql
# import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv() #load the env file 
from .config import Config #configurations



app = Flask(__name__) 

db = SQLAlchemy(app) #db csetup

csrf = CSRFProtect(app) #csrf token form page and from validation


# app.config['DATABASE_HOST'] = os.environ.get('DATABASE_HOST') or '192.168.64.2'
# app.config['DATABASE_USER'] = os.environ.get('DATABASE_USER') or 'root'
# app.config['DATABASE_PASSWORD'] = os.environ.get('DATABASE_PASSWORD') or ''
# app.config['DATABASE_NAME'] = os.environ.get('DATABASE_NAME') or 'duroad'

# Connect to mysql database
# def connectdb():
#     db = mysql.connect(host= app.config['DATABASE_HOST'], 
#                     database= app.config['DATABASE_NAME'],
#                     user= app.config['DATABASE_USER'],
#                     password= app.config['DATABASE_PASSWORD'])  
#     return db

# db = connectdb()

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# api = restful.Api(app, decorators=[csrf.exempt])
# app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config.from_object(Config)
from app import views, models
# from app.models import *