from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
database = SQLAlchemy(app)
manager = LoginManager(app)

with app.app_context():
    database.create_all()
