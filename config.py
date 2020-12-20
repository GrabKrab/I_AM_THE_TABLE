"""Flask app configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, 'secret_key.env'))


class Config:
    """ Base config """
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    SESSION_COOKIE_NAME = 'session'
    SECRET_KEY = environ.get('SECRET_KEY')
    print(SESSION_COOKIE_NAME)
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
    # DATABASE_URI = environ.get('DEV_DATABASE_URI')

    # Flask-SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:////database/users.db'
    # SQLALCHEMY_ECHO = False
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_BINDS = {
    #     f'{table.name}': 'sqlite:////database/table1.db'
    # }


# class ProdConfig(Config):
#     FLASK_ENV = 'production'
#     DEBUG = True
#     TESTING = True
#     # DATABASE_URI = environ.get('DEV_DATABASE_URI')