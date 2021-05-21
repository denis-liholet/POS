import unittest

from faker import Faker
from flask import request

from models.model import *
from pos import app
from service.admin_utils import *
from views import admin, user, staff, error


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
        role=fake.pybool()
    )
    return pizza, ingredient, user


class TestAdminUtils(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.config['TESTING'] = True
            app.config['CSRF_ENABLED'] = False
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources/test.db'
            self.app = app.test_client()
            database.init_app(app)
            database.create_all()
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
        assert if_empty(None, 1) == 1
        assert if_empty(1, None) == 1

    def test_get_all_items(self):
        with app.app_context():
            assert len(get_all_items(Pizza)) == 5
            assert len(get_all_items(Ingredient)) == 5
            assert len(get_all_items(User)) == 5

    def test_add_new_pizza(self):
        with app.app_context():
            with app.test_request_context(data={
                'name': 'test_name',
                'description': 'test_description',
                'image': 'test_path',
                'price': ''}
            ):
                add_new_pizza(request)
                assert Pizza.query.count() == 6
                item = Pizza.query.filter_by(name='test_name').first()
                assert item.description == 'test_description'
                assert item.image == 'test_path'
                assert item.price == 0

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
                assert item.name == 'test_name'
                assert item.description == 'test_description'
                assert item.image == 'test_path'
                assert item.price == 777

    def test_del_pizza(self):
        with app.app_context():
            with app.test_request_context(data={'id': 1}):
                del_pizza(request)
                assert Pizza.query.count() == 4

    def test_delete_user(self):
        with app.app_context():
            with app.test_request_context(data={'id': 1}):
                delete_user(request)
                assert User.query.count() == 4


if __name__ == '__main__':
    unittest.main()
