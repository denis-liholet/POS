from flask import flash, redirect, url_for

from models.model import Pizza, User
from app import database


def if_empty(new_value, old_value):
    """
    This function returns an old value if a new one is empty
    :param new_value: an incoming value which is trying out
    :param old_value: previous value
    :return: a new value if it was not empty
    """
    if new_value:
        return new_value
    return old_value


def get_all_items(model_class):
    """
    This function returns all the rows from table in database,
    similar to "SELECT * FROM table_name"
    :param model_class: ORM-based class of model
    :return: all data from the table
    """
    return model_class.query.all()


def add_new_pizza(request) -> None:
    """
    This function adds a new item to Pizza table using the request parameter "form"
    :param request: request by POST method
    :return: None
    """
    name = request.form['name']
    description = request.form['description']
    image = request.form['image']

    not_unique = Pizza.query.filter_by(name=name).first()

    if not_unique:
        return flash('Pizza name should be an unique')
    else:
        try:
            price = round(float(request.form['price']), 2)
        except ValueError:
            flash('Check your input on the price field. The price could be only in a number format.'
                  'The pizza price has been set to 0.00 hrn, you should change this value.')
            price = 0
        pizza = Pizza(name=name, description=description, price=price, image=image)

        database.session.add(pizza)
        database.session.commit()

        flash(f'Pizza "{pizza.name}" has been added.')


def update_pizza(request, pizza):
    """
    This function updates exist item fields. Checks input value for the price field by handling
    VallueError. If it raises in the case of non-digit value input then the previous price value will not be changed
    :param request: request by POST method
    :param pizza: row from Pizza table
    :return: redirect to "/db_edit" endpoint
    """
    new_name = request.form['name']
    new_description = request.form['description']
    new_image = request.form['image']

    try:
        new_price = round(float(request.form['price']), 2)
    except ValueError:
        flash('Check your input on the price field. The price could only be in a number format. '
              'The pizza price will not be changed')
        new_price = pizza.price

    pizza.name = if_empty(new_name, pizza.name)
    pizza.description = if_empty(new_description, pizza.description)
    pizza.price = if_empty(new_price, pizza.price)
    pizza.image = if_empty(new_image, pizza.image)

    database.session.commit()

    flash(f'Pizza "{pizza.name}" has been updated.')

    return redirect(url_for('db_edit'))


def del_pizza(request) -> None:
    """
    This function deletes an item from Pizza table using a request parameter "form"
    :param request: request by POST-method
    :return: None
    """
    pizza_id = int(request.form.get('id'))
    pizza = Pizza.query.filter_by(id=pizza_id).first()

    database.session.delete(pizza)
    database.session.commit()

    flash(f'Pizza "{pizza.name}" has been deleted.')


def delete_user(request) -> None:
    """
    This function deletes an item from User table using a request parameter "form".
    :param request: request by POST-method
    :return: None
    """
    user_id = int(request.form['id'])
    user = User.query.filter_by(id=user_id).first()

    database.session.delete(user)
    database.session.commit()

    flash(f'User "{user.name} {user.last_name}" has been deleted.')
