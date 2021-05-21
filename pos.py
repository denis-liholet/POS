from flask import Flask

from config import Configuration
from models.model import database, manager

app = Flask(__name__)
app.config.from_object(Configuration)
database.init_app(app)
manager.init_app(app)
# with app.app_context():
#     database.create_all()
