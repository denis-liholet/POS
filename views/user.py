from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_user, current_user
from sqlalchemy import desc
from werkzeug.security import check_password_hash

from app import app
from orm.model import database, Pizza, Ingredient, Order, User
from service.admin_utils import get_all_items
from service.user_utils import sign_up_user, pizza_rate


# -------------------------------- USER PART -----------------------------------------


@app.after_request
def redirect_to_signin(response):
    # this endpoint redirects an user to login page if not logged in
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response


@app.route('/')
@app.route('/index')
def index():
    # start page
    return render_template('index.html')


@app.route('/sign_up', methods=('GET', 'POST'))
def sign_up():
    # this endpoint registers a new user using the data from request.
    if request.method == 'POST':
        sign_up_user(request)
        return redirect(url_for('login'))
    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # this endpoint authorizes an user in system
    user_login = request.form.get('login')
    user_password = request.form.get('password')

    if user_login and user_password:
        user = User.query.filter_by(login=user_login).first()

        if user and check_password_hash(user.password, user_password):
            login_user(user)
            user_role = User.query.filter_by(login=user_login).first().role
            if user_role:
                return redirect(url_for('admin'))
            return redirect(url_for('all_orders_staff'))
        else:
            flash('Login or password is not correct')

    return render_template('login.html')


@app.route('/logout')
def logout():
    # redirecting an user to the start page after logging out
    logout_user()
    return redirect(url_for('index'))


@app.route('/all_orders')
def all_orders():
    # shows the list of all current orders
    orders = get_all_items(Order)
    return render_template('all_orders_user.html', orders=orders)


@app.route('/pizza_list', methods=('GET', 'POST'))
def pizza_list():
    goods = ''
    # shows the list of all pizzas
    if request.method == 'GET':
        goods = get_all_items(Pizza)

    # shows the pizzas list in chosen order
    if request.method == 'POST':

        # sorting by price
        if request.form.get('name') == 'price':
            goods = Pizza.query.order_by(Pizza.price)

        # sorting by name
        if request.form.get('name') == 'name':
            goods = Pizza.query.order_by(Pizza.name)

        # sorting by rate
        if request.form.get('name') == 'rate':
            goods = Pizza.query.order_by(desc(Pizza.rate))

    return render_template('pizza_list.html', goods=goods)


@app.route('/pizza_detail/<int:pizza_id>')
def pizza_detail(pizza_id):
    # shows pizza details like name, price, ingredients etc.
    pizza = Pizza.query.filter_by(id=pizza_id).first_or_404()
    ingredient = get_all_items(Ingredient)
    return render_template('pizza_detail.html', pizza=pizza, ingredient=ingredient)


@app.route('/add_order/<int:pizza_id>', methods=('GET', 'POST'))
def add_order(pizza_id):
    # adds the pizza with chosen ingredients to the order
    pizza = Pizza.query.filter_by(id=pizza_id).first()
    content = request.values

    # ingredients info formation
    ing_list = []
    ing_price = 0
    for item in content:
        ing_list.append(item)
        ingredient = Ingredient.query.filter_by(type=item).first()
        ing_price += ingredient.price
    ingredient = ', '.join(ing_list)

    # creating a new order
    if request.method == 'POST':
        order = Order(
            order_pizza=pizza_id,
            ingredient=ingredient,
            total_amount=pizza.price + ing_price
        )
        database.session.add(order)
        database.session.commit()

        return render_template('order_info.html', pizza=pizza, order=order)


@app.route('/add_rate/<int:pizza_id>', methods=('GET', 'POST'))
def add_rate(pizza_id):
    # setting "like" or "dislike" for the pizza rate
    pizza = Pizza.query.filter_by(id=pizza_id).first()
    if request.method == 'POST':
        pizza_rate(request, pizza)

    return redirect(url_for('pizza_detail', pizza_id=pizza_id))
