import unittest

from faker import Faker
from flask import request

from models.model import Ingredient, Pizza, User
from app import app, database
from service.admin_utils import if_empty, get_all_items, add_new_pizza, update_pizza, del_pizza, delete_user
from service.user_utils import pizza_rate, sign_up_user


def populate_test_db():
    fake = Faker()
    pizza = Pizza(
        name=fake.city(),
        description=fake.address(),
        price=fake.random_digit(),
        image=fake.text()
    )
    ingredient = Ingredient(
        type=fake.name(),
        price=fake.random_digit()
    )
    user = User(
        name=fake.city(),
        last_name=fake.city(),
        login=fake.city(),
        password=fake.random_digit(),
        role=fake.pybool(),
    )
    return pizza, ingredient, user


class TestAdminUtils(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.config['TESTING'] = True
            app.config['CSRF_ENABLED'] = False
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources/test.db'
            self.app = app.test_client()
            database.create_all()
            database.init_app(app)
            for _ in range(5):
                result = populate_test_db()
                for item in result:
                    database.session.add(item)
            database.session.commit()

    def tearDown(self):
        with app.app_context():
            database.session.remove()
            database.drop_all()

    def test_if_empty_1(self):
        self.assertEqual(if_empty(None, 1), 1)
        self.assertEqual(if_empty(1, None), 1)

    def test_get_all_items(self):
        with app.app_context():
            self.assertEqual(len(get_all_items(Pizza)), 5)
            self.assertEqual(len(get_all_items(Ingredient)), 5)
            self.assertEqual(len(get_all_items(User)), 5)

    def test_add_new_pizza(self):
        with app.app_context():
            with app.test_request_context(data={
                'name': 'test_name',
                'description': 'test_description',
                'image': 'test_path',
                'price': ''}
            ):
                add_new_pizza(request)
                self.assertEqual(Pizza.query.count(), 6)
                item = Pizza.query.filter_by(name='test_name').first()
                self.assertEqual(item.description, 'test_description')
                self.assertEqual(item.image, 'test_path')
                self.assertEqual(item.price, 0)
                self.assertEqual(item.rate, 0)

    def test_update_pizza(self):
        with app.app_context():
            with app.test_request_context(data={
                'name': 'test_name',
                'description': 'test_description',
                'image': 'test_path',
                'price': '777'}
            ):
                item = Pizza.query.filter_by(id=1).first()
                update_pizza(request, item)
                self.assertEqual(item.name, 'test_name')
                self.assertEqual(item.description, 'test_description')
                self.assertEqual(item.image, 'test_path')
                self.assertEqual(item.price, 777)

    def test_del_pizza(self):
        with app.app_context():
            with app.test_request_context(data={'id': 1}):
                del_pizza(request)
                self.assertEqual(Pizza.query.count(), 4)

    def test_delete_user(self):
        with app.app_context():
            with app.test_request_context(data={'id': 1}):
                delete_user(request)
                self.assertEqual(User.query.count(), 4)

    def test_pizza_rate(self):
        with app.app_context():
            item = Pizza.query.filter_by(id=1).first()
            with app.test_request_context(data={'like': 'set'}):
                pizza_rate(request, item)
                self.assertEqual(item.rate, 1)
                pizza_rate(request, item)
                pizza_rate(request, item)
                self.assertEqual(item.rate, 3)
            with app.test_request_context(data={'dislike': 'set'}):
                pizza_rate(request, item)
                self.assertEqual(item.rate, 2)

    def test_sign_up_user(self):
        with app.app_context():
            with app.test_request_context(data={
                'login': 'test',
                'password': '0000',
                'password2': '0000',
                'name': 'Name',
                'last_name': 'Last',
                'role': 'True'
            }):
                sign_up_user(request)
                self.assertEqual(User.query.count(), 6)
                user = User.query.filter_by(name='Name').first().name
                self.assertEqual(user, 'Name')
            with app.test_request_context(data={
                'login': 'test',
                'password': '0000',
                'password2': '1111',
                'name': 'Name',
                'last_name': 'Last',
                'role': 'True'
            }):
                self.assertEqual(User.query.count(), 6)


if __name__ == '__main__':
    unittest.main()
