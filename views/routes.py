import flask_login
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from models.model import database, Pizza, Ingredient, User, Order


# -------------------------------- USER PART -----------------------------------------


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response


@app.route('/base')
def base():
    return render_template('base_user.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    act_login = request.form.get('login')
    act_password = request.form.get('password')
    act_password2 = request.form.get('password2')
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    role = True if request.form.get('role') == 'true' else False

    if request.method == 'POST':
        if not (act_login or act_password or act_password2):
            flash('Please fill all fields!')
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
            login_user(user.name)
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
    orders = Order.query.all()
    return render_template('all_orders_user.html', orders=orders)


@app.route('/pizza_list')
def pizza_list():
    goods = Pizza.query.all()
    return render_template('pizza_list.html', goods=goods)


@app.route('/pizza_detail/<int:pizza_id>')
def pizza_detail(pizza_id):
    pizza = Pizza.query.filter_by(id=pizza_id).first_or_404()
    ingredient = Ingredient.query.all()
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


# -------------------------------- STAFF PART -----------------------------------------


@app.route('/staff')
@login_required
def staff():
    return render_template('base_staff.html')


@app.route('/all_orders_staff')
@login_required
def all_orders_staff():
    print(flask_login)
    orders = Order.query.join(Pizza).add_column(Pizza.name)
    return render_template('all_orders_staff.html', orders=orders)


@app.route('/done/<int:order_id>', methods=('POST', 'GET'))
@login_required
def done(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404()
    print(flask_login.COOKIE_NAME)
    if request.method == 'POST':
        order.state = True
        # order.order_user =

        database.session.commit()
        return redirect(url_for('all_orders_staff'))


# -------------------------------- ADMIN PART -----------------------------------------


@app.errorhandler(500)
def internal_server_error():
    return 'Sorry, I`m just learning(', 500


@app.route('/admin')
@login_required
def admin():
    return render_template('base_admin.html')


@app.route('/all_orders_admin')
@login_required
def all_orders_admin():
    orders = Order.query.all()
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
        pizza = Pizza(
            name=request.form['name'],
            description=request.form['description'],
            price=round(float(request.form['price']), 2),
            image=request.form['image']
        )
        database.session.add(pizza)
        database.session.commit()

    return redirect(url_for('db_edit'))


def if_empty(new_value, old_value):
    if new_value:
        return new_value
    return old_value


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
