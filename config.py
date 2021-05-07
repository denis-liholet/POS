

class Configuration:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static/pos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USERNAME = 'owner'
    PASSWORD = '1'
    SECRET_KEY = '123'
