from flask import Flask, render_template, request, session, redirect, url_for
from models.model import database, Pizza, Ingredient, Credential
from config import Configuration
import hashlib

app = Flask(__name__)
app.config.from_object(Configuration)
database.init_app(app)


def crypto(phrase):
    return hashlib.md5(phrase.encode()).hexdigest()


@app.errorhandler(500)
def internal_server_error(e):
    return 'Sorry, I`m just learning(', 500


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
        if data is not None and data.password == crypto(user_password):
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


@app.route('/admin')
def admin():
    return render_template('base_admin.html')


@app.route('/staff')
def staff():
    return render_template('base_staff.html')


@app.route('/all_orders')
def all_orders():
    return render_template('all_orders_user.html')


@app.route('/all_orders_staff')
def all_orders_staff():
    return render_template('all_orders_staff.html')


@app.route('/pizza_detail/<int:pizza_id>')
def pizza_detail(pizza_id):
    pizza = Pizza.query.filter_by(pizza_id=pizza_id).first_or_404()
    ingredient = Ingredient.query.all()
    return render_template('pizza_detail.html', pizza=pizza, ingredient=ingredient)


@app.route('/pizza_list')
def pizza_list():
    goods = Pizza.query.all()
    return render_template('pizza_list.html', goods=goods)


@app.route('/db_edit')
def db_edit():
    goods = Pizza.query.all()
    return render_template('db_edit.html', goods=goods)


@app.route('/db_edit', methods=('GET', 'POST'))
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


@app.route('/del_item', methods=('POST',))
def del_item():
    pizza_id = int(request.form['pizza_id'])
    pizza = Pizza.query.filter_by(pizza_id=pizza_id).first()
    database.session.delete(pizza)
    database.session.commit()
    return redirect(url_for('db_edit'))


def if_empty(new_value, old_value):
    if new_value:
        print('new')
        return new_value
    print('old')
    return old_value


@app.route('/update_item/<int:pizza_id>', methods=('POST', 'GET'))
def update_item(pizza_id):
    pizza = Pizza.query.filter_by(pizza_id=pizza_id).first_or_404()

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


@app.route('/ingredient_list')
def ingredient_list():
    ingredient = Ingredient.query.all()
    return render_template('ingredient_list.html', ingredient=ingredient)


@app.route('/user_list')
def user_list():
    users = Credential.query.all()
    return render_template('user_list.html', users=users)


@app.route('/del_user', methods=('POST',))
def del_user():
    credential_id = int(request.form['credential_id'])
    user = Credential.query.filter_by(credential_id=credential_id).first()
    database.session.delete(user)
    database.session.commit()
    return redirect(url_for('user_list'))


@app.route('/user_list', methods=('GET', 'POST'))
def add_user():
    if request.method == 'POST':
        role = True if request.form['role'] == 'true' else False

        user = Credential(
            name=request.form['name'],
            last_name=request.form['last_name'],
            login=request.form['login'],
            password=crypto(request.form['password']),
            role=role,
        )
        database.session.add(user)
        database.session.commit()

    return redirect(url_for('user_list'))


if __name__ == '__main__':
    app.run()
