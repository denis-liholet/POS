from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_user
from sqlalchemy import desc
from werkzeug.security import check_password_hash, generate_password_hash

from models.model import database, Pizza, Ingredient, Order, User
from pos import app
from service.admin_utils import get_all_items


# -------------------------------- USER PART -----------------------------------------


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/sign_up', methods=('GET', 'POST'))
def sign_up():
    """
    This endpoint registers a new user using the data from request. If there is no data in login, password
    or password2 fields user has to fill required fields up again. If password and password2 do not
    match the user has to retype the passwords. If an entered login already exists the user has to choose another one.
    If all request values are correct - a new user will be added to database.
    The password will be encrypted by SHA256 algorithm
    """
    act_login = request.form.get('login')
    act_password = request.form.get('password')
    act_password2 = request.form.get('password2')
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    role = True if request.form.get('role') == 'true' else False

    if request.method == 'POST':
        if_login_exist = User.query.filter_by(login=act_login).first()
        if not act_login or not act_password or not act_password2:
            flash('Please fill all fields up!')
        elif if_login_exist:
            flash('This login already exists! Try another one')
        elif act_password != act_password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(act_password)
            new_user = User(
                login=act_login,
                password=hash_pwd,
                name=name,
                last_name=last_name,
                role=role
            )
            database.session.add(new_user)
            database.session.commit()
            return redirect(url_for('login'))
    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    act_login = request.form.get('login')
    act_password = request.form.get('password')

    if act_login and act_password:
        user = User.query.filter_by(login=act_login).first()

        if user and check_password_hash(user.password, act_password):
            login_user(user)
            user_role = User.query.filter_by(login=act_login).first().role
            if user_role:
                return redirect(url_for('admin'))
            return redirect(url_for('all_orders_staff'))
        else:
            flash('Login or password is not correct')

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/all_orders')
def all_orders():
    orders = get_all_items(Order)
    return render_template('all_orders_user.html', orders=orders)


@app.route('/pizza_list', methods=('GET', 'POST'))
def pizza_list():
    if request.method == 'GET':
        goods = get_all_items(Pizza)
    if request.method == 'POST':
        if request.form.get('name') == 'price':
            goods = Pizza.query.order_by(Pizza.price)
        if request.form.get('name') == 'name':
            goods = Pizza.query.order_by(Pizza.name)
        if request.form.get('name') == 'rate':
            goods = Pizza.query.order_by(desc(Pizza.rate))

    return render_template('pizza_list.html', goods=goods)


@app.route('/pizza_detail/<int:pizza_id>')
def pizza_detail(pizza_id):
    pizza = Pizza.query.filter_by(id=pizza_id).first_or_404()
    ingredient = get_all_items(Ingredient)
    return render_template('pizza_detail.html', pizza=pizza, ingredient=ingredient)


@app.route('/add_order/<int:pizza_id>', methods=('GET', 'POST'))
def add_order(pizza_id):
    pizza = Pizza.query.filter_by(id=pizza_id).first()
    content = request.values
    ing_list = []
    ing_price = 0
    for item in content:
        ing_list.append(item)
        ingredient = Ingredient.query.filter_by(type=item).first()
        ing_price += ingredient.price
    ingredient = ', '.join(ing_list)

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
    pizza = Pizza.query.filter_by(id=pizza_id).first()
    if request.method == 'POST':
        if request.form.get('like') == '1':
            pizza.rate += 1
        if request.form.get('dislike') == '2':
            pizza.rate -= 1

        database.session.commit()

    return redirect(url_for('pizza_detail', pizza_id=pizza_id))
