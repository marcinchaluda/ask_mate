from flask import render_template, redirect, request, session

def is_user_loggedin(template: str, data_id = None, data_type = None):
    if request.method == "GET":
        if 'email' not in session:
            return redirect('/login')
        return render_template('modify_data_layout/'+template, data_id=data_id, data_type=data_type)