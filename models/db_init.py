from app import app, database


def create_database():
    with app.app_context():
        database.create_all()


if __name__ == '__main__':
    create_database()
