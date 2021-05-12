from flask import Flask
from flask_login import LoginManager

from config import Configuration
from models.model import database

app = Flask(__name__)
app.config.from_object(Configuration)
database.init_app(app)
#manager = LoginManager(app)

