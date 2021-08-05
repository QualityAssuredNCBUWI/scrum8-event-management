""" Config for Duroad app
"""
import os

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    SQLALCHEMY_DATABASE_URI = os.environ.get('MY_DATABASE_URL')  
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed
    
    PROFILE_UPLOAD_FOLDER = os.environ.get('PROFILE_UPLOAD_FOLDER') or 'files/upload/profile'
    EVENT_UPLOAD_FOLDER = os.environ.get('EVENT_UPLOAD_FOLDER') or 'files/upload/event'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class DevelopmentConfig(Config):
    """Development Config that extends the Base Config Object"""
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    """Production Config that extends the Base Config Object"""
    DEBUG = False
