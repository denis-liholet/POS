from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app import app
from models.model import database, Pizza, User, Order


# -------------------------------- STAFF PART -----------------------------------------


@app.route('/staff')
@login_required
def staff():
    return render_template('base_staff.html')


@app.route('/all_orders_staff')
@login_required
def all_orders_staff():
    orders = Order.query.join(Pizza).add_column(Pizza.name)
    return render_template('all_orders_staff.html', orders=orders)


@app.route('/done/<int:order_id>', methods=('POST', 'GET'))
@login_required
def done(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404()
    employee = User.query.filter_by(login=str(current_user)).first_or_404()
    if request.method == 'POST':
        order.state = True
        order.order_user = employee.id
        employee.completed_orders += 1
        database.session.commit()
        return redirect(url_for('all_orders_staff'))