from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
manager = LoginManager()


class Pizza(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), unique=True, nullable=False)
    description = database.Column(database.String(100), unique=False, nullable=False)
    price = database.Column(database.Numeric(scale=2), nullable=False)
    image = database.Column(database.String(100))
    orders = database.relationship('Order', backref='pizza')

    def __repr__(self):
        return f'{self.name}, {self.price}'


class Ingredient(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    type = database.Column(database.String(100), unique=True, nullable=False)
    price = database.Column(database.Numeric(scale=2), nullable=False)

    def __repr__(self):
        return f'{self.type}, {self.price}'


class Order(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    order_pizza = database.Column(database.Integer, database.ForeignKey('pizza.id'), nullable=True)
    ingredient = database.Column(database.String(300), nullable=True)
    total_amount = database.Column(database.Numeric(scale=2), nullable=True)
    order_user = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=True)
    state = database.Column(database.BOOLEAN, default=False)

    def __repr__(self):
        return f'{self.id}, {self.order_pizza}, {self.ingredient}, {self.total_amount}, {self.state}'


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String, nullable=False)
    last_name = database.Column(database.String, nullable=False)
    login = database.Column(database.String(64), unique=True, nullable=False)
    password = database.Column(database.String(128), nullable=False)
    role = database.Column(database.Boolean, default=False)
    completed_orders = database.Column(database.Integer, default=0)
    orders = database.relationship('Order', backref='user')

    def __repr__(self):
        return f'{self.name}'


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
