from flask import Flask

from models.model import database, manager

app = Flask(__name__)
app.config.from_object('config')
database.init_app(app)
manager.init_app(app)

from views import admin, staff, user, error

if __name__ == '__main__':
    app.run()
