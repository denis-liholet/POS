class Configuration:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///resources/pos.db'
    SQLALCHEMY_MIGRATE_REPO = '/migrations'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'some secret salt)'
