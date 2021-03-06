import datetime
import os.path

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from orm.model import Ingredient, Order, Pizza, User
from app import app
from service.admin_utils import get_all_items, add_new_pizza, update_pizza, \
    del_pizza, delete_user, database_copy, database_restore


# -------------------------------- ADMIN PART -----------------------------------------


@app.route('/admin')
@login_required
def admin():
    # start page for authorized "Admin role" users
    return render_template('base_admin.html')


@app.route('/all_orders_admin')
@login_required
def all_orders_admin():
    # displays the completed orders list
    orders = Order.query.join(User, Pizza).add_column(User.name)
    return render_template('all_orders_admin.html', orders=orders)


@app.route('/db_edit')
@login_required
def db_edit():
    # database editor page
    goods = get_all_items(Pizza)
    return render_template('db_edit.html', goods=goods)


@app.route('/db_edit', methods=('GET', 'POST'))
@login_required
def add_new():
    # adds a new pizza to database
    if request.method == 'POST':
        add_new_pizza(request)
    return redirect(url_for('db_edit'))


@app.route('/update_item/<int:pizza_id>', methods=('POST', 'GET'))
@login_required
def update_item(pizza_id):
    # updates an existing pizza data
    pizza = Pizza.query.filter_by(id=pizza_id).first_or_404()
    if request.method == 'POST':
        update_pizza(request, pizza)
    return render_template('update_item.html', pizza=pizza)


@app.route('/del_item', methods=('POST', 'GET'))
@login_required
def del_item():
    # deletes the pizza
    del_pizza(request)
    return redirect(url_for('db_edit'))


@app.route('/ingredient_list')
@login_required
def ingredient_list():
    # ingredients list page
    ingredient = get_all_items(Ingredient)
    return render_template('ingredient_list.html', ingredient=ingredient)


@app.route('/user_list')
@login_required
def user_list():
    # users list page
    users = get_all_items(User)
    return render_template('user_list.html', users=users)


@app.route('/del_user', methods=('POST',))
@login_required
def del_user():
    # deletes the user
    if request.method == 'POST':
        delete_user(request)
    return redirect(url_for('user_list'))


@app.route('/database_manage', methods=['GET', 'POST'])
@login_required
def database_manage():
    file_info = ''
    # collecting the file information
    try:
        file = os.path.getmtime('resources/db_copy.db')
        file_info = datetime.datetime.fromtimestamp(file).strftime('%d-%m-%Y %H:%M:%S')
    except FileNotFoundError:
        flash('You don`t have a backup yet. Make copy first')

    # parsing the request values
    if request.method == 'POST':
        option = request.form.get('name')
        if option == 'copy':
            database_copy()
            flash(f'Database copy has been successfully made')
        if option == 'restore':
            database_restore()
            flash(f'Database has been restored')

    return render_template('database_manage.html', file_info=file_info)
