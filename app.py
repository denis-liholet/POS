from flask import Flask, render_template, request, session, redirect, url_for
from models.model import database, Pizza, Ingredient, Credential
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

database.init_app(app)


@app.route('/base')
def base():
    return render_template('base_user.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_name = request.form['username']
        user_password = request.form['password']
        data = Credential.query.filter_by(login=user_name).first()
        if data is not None and data.password == user_password:
            if data.role:
                session['logged_in'] = True
                return redirect(url_for('admin'))
            else:
                session['logged_in'] = False
                return redirect(url_for('staff'))
        else:
            error = 'Wrong username or password!'
    return render_template('login.html', error=error)


@app.route('/all_orders_admin')
def all_orders_admin():
    return render_template('all_orders_admin.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/order')
def order():
    goods = Pizza.query.all()
    return render_template('order.html', goods=goods)


@app.route('/order_details')
def order_details():
    return render_template('order_details.html')


@app.route('/admin')
def admin():
    return render_template('base_admin.html')


@app.route('/staff')
def staff():
    return render_template('base_staff.html')


@app.route('/all_orders')
def all_orders():
    return render_template('all_orders.html')


@app.route('/all_orders_staff')
def all_orders_staff():
    return render_template('all_orders_staff.html')


@app.route('/pizza_detail/<int:pizza_id>')
def pizza_detail(pizza_id):
    pizza = Pizza.query.filter_by(pizza_id=pizza_id).first_or_404()
    return render_template('pizza_detail.html', pizza=pizza)


@app.route('/pizza_list')
def pizza_list():
    goods = Pizza.query.all()
    return render_template('pizza_list.html', goods=goods)


@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    if not session.get('logged_in', False):
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('add_new.html')
    elif request.method == 'POST':
        pizza = Pizza(
            name=request.form['name'],
            description=request.form['description'],
            price=round(float(request.form['price']), 2)
        )

    database.session.add(pizza)
    database.session.commit()

    return redirect(url_for('staff'))


@app.route('/ingredient_list')
def ingredient_list():
    goods = Ingredient.query.all()
    return render_template('ingredient_list.html', goods=goods)
