import model.data_manager as data_manager
from flask import render_template, redirect, request, Blueprint, url_for, session
from psycopg2 import errors
from model.util import generate_seconds_since_epoch
from markupsafe import escape
user_data = Blueprint('user_operations', __name__)


@user_data.route('/registration', methods=['GET', 'POST'])
def show_signup_form():
    if 'username' in session:
        # let user know they need to log out first
        return render_template('modify_data_layout/add_user.html', user=escape(session['username']))
    if 'mail_already_taken' in request.args:
        return render_template('modify_data_layout/add_user.html', mail_already_taken=True)
    if request.method == 'POST':
        return redirect(url_for('user_operations.process_registration'), code=307)
    return render_template('modify_data_layout/add_user.html')


@user_data.route('/registration/add_user', methods=['POST'])
def process_registration():
    new_user_data = {}
    new_user_data.update({'user_id': request.form['username']})
    new_user_data.update({'password': request.form['password']})
    new_user_data.update({'user_name': request.form['first_name'] + ' ' + request.form['last_name']})
    new_user_data.update({'submission_time': generate_seconds_since_epoch()})
    try:
        data_manager.add_new_user(new_user_data)
    except errors.UniqueViolation:
        return redirect(url_for('user_operations.show_signup_form', mail_already_taken=True))
    return redirect(url_for('home'))
