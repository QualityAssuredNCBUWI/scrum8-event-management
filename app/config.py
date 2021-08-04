""" Config for Duroad app
"""
import os

class Config(object):
    """Base Config Object"""
    DEBUG = False
<<<<<<< HEAD
    SECRET_KEY = os.environ.get('SECRET_KEY') or ' '
    SQLALCHEMY_DATABASE_URI = os.environ.get('MY_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    # This is just here to suppress a warning from SQLAlchemy as it will soon be removed 
=======
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('MY_DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed
>>>>>>> f50a7535eda6dce98df9de7155a7219b8f666162
    PROFILE_UPLOAD_FOLDER = os.environ.get('PROFILE_UPLOAD_FOLDER') or './profileUploads'
    EVENT_UPLOAD_FOLDER = os.environ.get('EVENT_UPLOAD_FOLDER') or './eventUploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class DevelopmentConfig(Config):
    """Development Config that extends the Base Config Object"""
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    """Production Config that extends the Base Config Object"""
    DEBUG = False
