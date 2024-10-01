from flask import Blueprint
from flask import flash
from flask import request, render_template, url_for, redirect
"""############ import models  #############"""
from authentication.database.model import Users
from authentication.database.extensions import db
from authentication.database.extensions import OTP, session
"""############ import uconra  #############"""
from uconra.register import Register


reset_password_bp = Blueprint('reset_password', __name__,
                              template_folder='templates',
                              static_folder='static',
                              static_url_path='/login/static'
                              )

@reset_password_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':

        # Get user's new password, and confirm password from the user input from the form
        new_password = request.form.get('new_password', False)
        confirm_new_password = request.form.get('confirm_new_password', False)

        if new_password == confirm_new_password:
            if 'user_from_email' in session:

                hash_password = Register()
                hashed_password = hash_password.userPassword(confirm_new_password)

                user_from_email = session['user_from_email']
                print(user_from_email)
                user_reset_pw = Users.query.filter_by(email=user_from_email).first()
                user_reset_pw.password = hashed_password
                db.session.commit()
                flash('Password  changed successfully. ')
            return redirect(url_for('fruutty_token.index', email=user_from_email))
        else:
            print('Password do not match. Enter matching passwords')
            flash('Password do not match. Enter matching passwords')

    return render_template('reset_password.html', )