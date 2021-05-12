from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class Pizza(database.Model):
    pizza_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), unique=True, nullable=False)
    description = database.Column(database.String(100), unique=False, nullable=False)
    price = database.Column(database.Numeric(scale=2), nullable=False)
    orders = database.relationship('Order', backref='pizza')
    image = database.Column(database.String(100))

    def __repr__(self):
        return f'{self.name}, {self.price}'


class Ingredient(database.Model):
    ingredient_id = database.Column(database.Integer, primary_key=True)
    type = database.Column(database.String(100), unique=True, nullable=False)
    price = database.Column(database.Numeric(scale=2), nullable=False)

    def __repr__(self):
        return f'{self.type}, {self.price}'


class Order(database.Model):
    order_id = database.Column(database.Integer, primary_key=True)
    order_pizza = database.Column(database.Integer, database.ForeignKey('pizza.pizza_id'), nullable=False)
    ingredient = database.Column(database.String(300), nullable=True)
    total_amount = database.Column(database.Numeric(scale=2), nullable=True)
    order_credential = database.Column(database.Integer, database.ForeignKey('user.user_id'), nullable=True)
    state = database.Column(database.BOOLEAN, default=False)

    def __repr__(self):
        return f'{self.order_id}, {self.order_pizza}, {self.ingredient}, {self.total_amount}, {self.state}'


class User(database.Model):
    user_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String, unique=False, nullable=False)
    last_name = database.Column(database.String, unique=False, nullable=False)
    login = database.Column(database.String, unique=True, nullable=False)
    password = database.Column(database.String, unique=False, nullable=False)
    role = database.Column(database.Boolean, default=False)
    orders = database.relationship('Order', backref='user')

    def __repr__(self):
        return f'{self.name, self.last_name, self.role}'
