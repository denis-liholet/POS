from pos import app, database
from views import *

if __name__ == '__main__':
    with app.app_context():
        database.create_all()
    app.run()
