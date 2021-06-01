from app import database


def order_done(order, employee) -> None:
    """
    This function shifts the order state from "Baking" to "Ready" by changing "order.state" value
    from False (default) to True and is increasing "completed_orders" by 1
    :param order: row from the Order table
    :param employee: row from the User table
    :return: None
    """
    order.state = True
    order.order_user = employee.id
    employee.completed_orders += 1

    database.session.commit()
