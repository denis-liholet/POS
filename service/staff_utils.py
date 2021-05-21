from pos import database


def order_done(order, employee):
    order.state = True
    order.order_user = employee.id
    employee.completed_orders += 1
    database.session.commit()
