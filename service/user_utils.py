from flask import flash
from werkzeug.security import generate_password_hash

from models.model import User
from app import database


def sign_up_user(request) -> None:
    """
    This function registers a new user using the data from request.
    If there is no data in login, password
    or password2 fields user has to fill required fields up again. If password and password2 do not
    match the user has to retype the passwords. If an entered login already exists the user has to choose another one.
    If all request values are correct - a new user will be added to database.
    The password will be encrypted by SHA256 algorithm
    :param request: request by POST method
    :return: None
    """

    # request parsing
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    role = True if request.form.get('role') == 'true' else False

    if_login_exist = User.query.filter_by(login=login).first()

    # validating of the incoming data
    if not login or not password or not password2:
        flash('Please fill all fields up!')
    elif if_login_exist:
        flash('This login already exists! Try another one')
    elif password != password2:
        flash('Passwords are not equal!')

    # creating a new user
    else:
        hash_pwd = generate_password_hash(password)
        new_user = User(
            login=login,
            password=hash_pwd,
            name=name,
            last_name=last_name,
            role=role
        )
        database.session.add(new_user)
        database.session.commit()
        flash(f'User {name} {last_name} has been created')
