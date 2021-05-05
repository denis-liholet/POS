class Configuration:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static/pos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USERNAME = 'owner'
    PASSWORD = 'owner'
    SECRET_KEY = '123'
