# flask app settings

DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///resources/pos.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'some secret salt)'

# mail settings

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'flask.logging@gmail.com'
MAIL_DEFAULT_SENDER = 'flask.logging@gmail.com'
MAIL_PASSWORD = 'Qaz123456!'
RECEPIENTS = ['palloncino.vin@gmail.com']
