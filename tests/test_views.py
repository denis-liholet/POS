import unittest

from pos import app
from views import admin, user, staff


class TestUserViews(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

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

    @unittest.skip
    def test_all_orders(self):
        response = self.app.get('/all_orders')
        self.assertEqual(response.status_code, 200)

    @unittest.skip
    def test_pizza_list(self):
        response = self.app.get('/pizza_list')
        self.assertEqual(response.status_code, 200)

    @unittest.skip
    def test_pizza_detail(self):
        response = self.app.get('/pizza_detail/1')
        self.assertEqual(response.status_code, 200)


class TestAdminViews(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.ctx = app.test_request_context()

    def test_admin(self):
        response = self.app.get('/admin')
        assert response.status_code == 302

    def test_all_orders_admin(self):
        response = self.app.get('/all_orders_admin')
        self.assertEqual(response.status_code, 302)

    def test_db_edit(self):
        response = self.app.get('/db_edit')
        self.assertEqual(response.status_code, 302)

    def test_ingredient_list(self):
        response = self.app.get('/ingredient_list')
        self.assertEqual(response.status_code, 302)

    def test_user_list(self):
        response = self.app.get('/user_list')
        self.assertEqual(response.status_code, 302)


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
