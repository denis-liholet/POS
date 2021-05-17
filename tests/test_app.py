import unittest

from pos import app
from service.if_empty import if_empty
from views import admin, user, staff, error


class TestFunctionality(unittest.TestCase):
    def test_if_empty_1(self):
        assert if_empty(None, 1) == 1

    def test_if_empty_2(self):
        assert if_empty(1, None) == 1


class TestUserViews(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/index')
        assert response.status_code == 200

    def test_sign_up(self):
        response = self.app.get('/sign_up')
        assert response.status_code == 200

    def test_login(self):
        response = self.app.get('/login')
        assert response.status_code == 200

    def test_logout(self):
        response = self.app.get('/logout')
        assert response.status_code == 302

    def test_all_orders(self):
        response = self.app.get('/all_orders')
        assert response.status_code == 200

    def test_pizza_list(self):
        response = self.app.get('/pizza_list')
        assert response.status_code == 200

    def test_pizza_detail(self):
        response = self.app.get('/pizza_detail/1')
        assert response.status_code == 200


class TestAdminViews(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.ctx = app.test_request_context()

    def tearDown(self):
        pass

    def test_admin(self):
        response = self.app.get('/admin')
        assert response.status_code == 302

    def test_all_orders_admin(self):
        response = self.app.get('/all_orders_admin')
        assert response.status_code == 302

    def test_db_edit(self):
        response = self.app.get('/db_edit')
        assert response.status_code == 302

    def test_ingredient_list(self):
        response = self.app.get('/ingredient_list')
        assert response.status_code == 302

    def test_user_list(self):
        response = self.app.get('/user_list')
        assert response.status_code == 302


class TestStaffViews(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.ctx = app.test_request_context()

    def tearDown(self):
        pass

    def test_staff(self):
        response = self.app.get('/staff')
        assert response.status_code == 302

    def all_orders_staff(self):
        response = self.app.get('/all_orders_staff')
        assert response.status_code == 302


if __name__ == '__main__':
    unittest.main()
