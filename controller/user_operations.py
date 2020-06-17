import model.user_manager as user_manager
import model.data_manager as data_manager
from flask import render_template, redirect, request, Blueprint, url_for, session
from psycopg2 import errors
from model.util import generate_seconds_since_epoch
from markupsafe import escape
import bcrypt
from werkzeug.exceptions import BadRequestKeyError
user_data = Blueprint('user_operations', __name__)


@user_data.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = user_manager.get_user_by_email(email)
        if email in user['email'] and verify_password(password, user['password']):
            session['email'] = request.form['email']
            return redirect(url_for('display_data'))
        message = 'Wrong email or password.'
    return render_template('login.html', message=message)


@user_data.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('display_data'))


def hash_password(plain_text_password):
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def verify_password(plain_text_password, hashed_password) -> bool:
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)  # RETURNS TRUE IF PASSWORDS MATCH


@user_data.route('/registration', methods=['GET', 'POST'])
def show_signup_form():
    if 'username' in session:
        return render_template('modify_data_layout/add_user.html', user=escape(session['username']))
    if 'mail_already_taken' in request.args:
        return render_template('modify_data_layout/add_user.html', mail_already_taken=True)
    if request.method == 'POST':
        return redirect(url_for('user_operations.process_registration'), code=307)
    return render_template('modify_data_layout/add_user.html')


@user_data.route('/registration/add_user', methods=['POST'])
def process_registration():
    new_user_data = {}
    try:
        new_user_data.update({'user_id': request.form['username']})
        new_user_data.update({'password': hash_password(request.form['password'])})
        new_user_data.update({'user_name': request.form['first_name'] + ' ' + request.form['last_name']})
        new_user_data.update({'submission_time': generate_seconds_since_epoch()})
    except BadRequestKeyError:
        return redirect(url_for('user_operations.show_signup_form'))
    try:
        user_manager.add_new_user(new_user_data)
    except errors.UniqueViolation:
        return redirect(url_for('user_operations.show_signup_form', mail_already_taken=True))
    return redirect(url_for('home'))


@user_data.route('/user/<user_id>')
@user_data.route('/user/')
def show_user_page(user_id=None):
    if user_id:
        user_headers = user_manager.USERS_HEADERS
        user = data_manager ?
        return render_template('display_data/user_page.html', user_id=user_id, user_headers=user_headers, user=user)
    return render_template('display_data/breaking.html')
