import model.user_manager as user_manager
from flask import render_template, redirect, request, Blueprint, session, url_for
user_data = Blueprint('user_data', __name__)


@user_data.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = user_manager.get_user_by_email(email)
        if email in user['email'] and password in user['password']:
            session['email'] = request.form['email']
            return redirect(url_for('display_data'))
        message = 'Wrong password.'

    return render_template('login.html', message=message)