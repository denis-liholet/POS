import unittest

from models.model import *
from pos import app
from service.staff_utils import *


def populate_test_db():
    order = Order(order_pizza=1, total_amount=50)
    emp = User(
        name='Chef',
        last_name='Test',
        login='login',
        password='pass',
        role=False
    )
    return order, emp


class TestStaffUtils(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.config['TESTING'] = True
            app.config['CSRF_ENABLED'] = False
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources/test.db'
            self.app = app.test_client()
            database.init_app(app)
            database.create_all()
            for _ in range(1):
                result = populate_test_db()
                for item in result:
                    database.session.add(item)
            database.session.commit()

    def tearDown(self):
        with app.app_context():
            database.session.remove()
            database.drop_all()

    def test_order_done(self):
        with app.app_context():
            employee = User.query.filter_by(role=False).first()
            order = Order.query.filter_by(total_amount=50).first()
            order_done(order, employee)
            assert order.state is True
            assert employee.completed_orders == 1


if __name__ == '__main__':
    unittest.main()
