from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models.model import Pizza, User, Order
from app import app
from service.staff_utils import order_done


# -------------------------------- STAFF PART -----------------------------------------


@app.route('/staff')
@login_required
def staff():
    # start page for authorized "Chef role" users
    return render_template('base_staff.html')


@app.route('/all_orders_staff')
@login_required
def all_orders_staff():
    # displays all active orders
    orders = Order.query.join(Pizza).add_column(Pizza.name)
    return render_template('all_orders_staff.html', orders=orders)


@app.route('/done/<int:order_id>', methods=('POST', 'GET'))
@login_required
def done(order_id):
    # shifts the order state from "Baking" to "Ready"
    order = Order.query.filter_by(id=order_id).first_or_404()
    employee = User.query.filter_by(login=str(current_user.login)).first_or_404()
    if request.method == 'POST':
        order_done(order, employee)
    return redirect(url_for('all_orders_staff'))
