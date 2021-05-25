from pos import database


def order_done(order, employee) -> None:
    """
    This function shifts order state from "Baking" to "Ready" by changing "order.state" value
    from False (default) to True and is increasing "completed_orders" by 1
    :param order: row from Order table
    :param employee: row from User table
    :return: None
    """
    order.state = True
    order.order_user = employee.id
    employee.completed_orders += 1

    database.session.commit()
