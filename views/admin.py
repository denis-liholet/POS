from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from pos import app
from models.model import database, Pizza, Ingredient, User, Order
from service.if_empty import if_empty


# -------------------------------- ADMIN PART -----------------------------------------


@app.route('/admin')
@login_required
def admin():
    return render_template('base_admin.html')


@app.route('/all_orders_admin')
@login_required
def all_orders_admin():
    orders = Order.query.join(User).add_column(User.name)
    return render_template('all_orders_admin.html', orders=orders)


@app.route('/db_edit')
@login_required
def db_edit():
    goods = Pizza.query.all()
    return render_template('db_edit.html', goods=goods)


@app.route('/db_edit', methods=('GET', 'POST'))
@login_required
def add_new():
    if request.method == 'POST':

        name = request.form['name']
        description = request.form['description']
        try:
            price = round(float(request.form['price']), 2)
        except ValueError:
            flash('Check your input for price field. Price could be a number format only. Pizza price has been '
                  'set to 0.00 hrn, you should change this value !!!')
            price = 0
        image = request.form['image']

        pizza = Pizza(
            name=name,
            description=description,
            price=price,
            image=image
        )
        database.session.add(pizza)
        database.session.commit()

    return redirect(url_for('db_edit'))


@app.route('/update_item/<int:pizza_id>', methods=('POST', 'GET'))
@login_required
def update_item(pizza_id):
    pizza = Pizza.query.filter_by(id=pizza_id).first_or_404()

    if request.method == 'POST':
        new_name = request.form['name']
        new_description = request.form['description']
        try:
            new_price = round(float(request.form['price']), 2)
        except ValueError:
            flash('Check your input for price field. Price could be a number format only. Pizza price has been '
                  'set to previous value.')
            new_price = pizza.price
        new_image = request.form['image']

        pizza.name = if_empty(new_name, pizza.name)
        pizza.description = if_empty(new_description, pizza.description)
        pizza.price = if_empty(new_price, pizza.price)
        pizza.image = if_empty(new_image, pizza.image)

        database.session.commit()
        return redirect(url_for('db_edit'))

    return render_template('update_item.html', pizza=pizza)


@app.route('/del_item', methods=('POST', 'GET'))
@login_required
def del_item():
    pizza_id = int(request.form.get('id'))
    pizza = Pizza.query.filter_by(id=pizza_id).first()
    database.session.delete(pizza)
    database.session.commit()
    return redirect(url_for('db_edit'))


@app.route('/ingredient_list')
@login_required
def ingredient_list():
    ingredient = Ingredient.query.all()
    return render_template('ingredient_list.html', ingredient=ingredient)


@app.route('/user_list')
@login_required
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/del_user', methods=('POST',))
@login_required
def del_user():
    user_id = int(request.form['id'])
    user = User.query.filter_by(id=user_id).first()
    database.session.delete(user)
    database.session.commit()
    return redirect(url_for('user_list'))
