import unittest

from faker import Faker

from app import app, database
from orm.model import Pizza, Ingredient, User


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


class TestUserViews(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.config['TESTING'] = True
            app.config['CSRF_ENABLED'] = False
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources/test.db'
            self.app = app.test_client()
            database.create_all()
            database.init_app(app)
            for _ in range(1):
                result = populate_test_db()
                for item in result:
                    database.session.add(item)
            database.session.commit()

    def tearDown(self):
        with app.app_context():
            database.session.remove()
            database.drop_all()

    def test_index(self):
        response = self.app.get('/index')
        self.assertEqual(response.status_code, 200)

    def test_sign_up(self):
        response = self.app.get('/sign_up')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.get('/login')
        assert response.status_code == 200

    def test_logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_all_orders(self):
        response = self.app.get('/all_orders')
        self.assertEqual(response.status_code, 200)

    def test_pizza_list(self):
        response = self.app.get('/pizza_list')
        self.assertEqual(response.status_code, 200)

    def test_pizza_detail(self):
        response = self.app.get('/pizza_detail/1')
        self.assertEqual(response.status_code, 200)


class TestAdminViews(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.ctx = app.test_request_context()

    def test_admin(self):
        response = self.app.get('/admin', follow_redirects=True)
        assert response.status_code == 200

    def test_all_orders_admin(self):
        response = self.app.get('/all_orders_admin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_db_edit(self):
        response = self.app.post('/db_edit', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_ingredient_list(self):
        response = self.app.get('/ingredient_list', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_user_list(self):
        response = self.app.get('/user_list', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_database_manage(self):
        response = self.app.post('/database_manage', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


class TestStaffViews(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_staff(self):
        response = self.app.get('/staff')
        self.assertEqual(response.status_code, 302)

    def all_orders_staff(self):
        response = self.app.get('/all_orders_staff')
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
