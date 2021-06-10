from flask import Flask

from orm.model import database, manager

app = Flask(__name__)
app.config.from_object('config')
database.init_app(app)
manager.init_app(app)

from views import *

if __name__ == '__main__':
    app.run()
