import unittest

from models.model import Order, Ingredient, Pizza, User
from app import app, database


def populate_test_db():
    pizza = Pizza(
        name='Some name',
        description='Some description',
        price=20,
        image='Some path'
    )
    ingredient = Ingredient(
        type='Some type',
        price=15
    )
    employee = User(
        name='User name',
        last_name='User last name',
        login='User login',
        password='User password',
        role=True
    )
    order = Order(
        order_pizza=1,
        ingredient='some ingredients',
        total_amount=50,
        order_user=1,
        state=False
    )
    return pizza, ingredient, employee, order


class TestAdminUtils(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.config['TESTING'] = True
            app.config['CSRF_ENABLED'] = False
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources/test.db'
            self.app = app.test_client()
            database.create_all()
            database.init_app(app)
            result = populate_test_db()
            for item in result:
                database.session.add(item)
            database.session.commit()

    def tearDown(self):
        with app.app_context():
            database.session.remove()
            database.drop_all()

    def test_user_repr(self):
        with app.app_context():
            data = str(User.query.filter_by(id=1).first())
            self.assertEqual(data, 'User name User last name')

    def test_order_repr(self):
        with app.app_context():
            data = str(Order.query.filter_by(id=1).first())
            self.assertEqual(data, '1, 1, some ingredients, 50.00, False')

    def test_pizza_repr(self):
        with app.app_context():
            data = str(Pizza.query.filter_by(id=1).first())
            self.assertEqual(data, 'Some name, 20.00')

    def test_ingredient_repr(self):
        with app.app_context():
            data = str(Ingredient.query.filter_by(id=1).first())
            self.assertEqual(data, 'Some type, 15.00')


if __name__ == '__main__':
    unittest.main()
