from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class Pizza(database.Model):
    pizza_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), unique=True, nullable=False)
    description = database.Column(database.String(100), unique=False, nullable=False)
    price = database.Column(database.Numeric(scale=2), nullable=False)
    image = database.Column(database.String(100), unique=True, nullable=True)

    def __repr__(self):
        return f'{self.name}, {self.price}'


class Ingredient(database.Model):
    ingredient_id = database.Column(database.Integer, primary_key=True)
    ingredient_type = database.Column(database.String(100), unique=True, nullable=False)
    ingredient_price = database.Column(database.Numeric(scale=2), nullable=False)

    def __repr__(self):
        return f'{self.ingredient_type}, {self.ingredient_price}'


class Order(database.Model):
    order_id = database.Column(database.Integer, primary_key=True)
    details = database.Column(database.String(300), nullable=False)
    total_amount = database.Column(database.Numeric(scale=2), nullable=False)
    state = database.Column(database.BOOLEAN, default=False)

    def __repr__(self):
        return f'{self.order_id}, {self.details}, {self.total_amount}, {self.state}'


class Credential(database.Model):
    credential_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String, unique=False, nullable=False)
    last_name = database.Column(database.String, unique=False, nullable=False)
    login = database.Column(database.String, unique=True, nullable=False)
    password = database.Column(database.String, unique=False, nullable=False)
