import jwt
from flask import Flask
from flask import flash, jsonify
from flask import Blueprint
from functools import wraps
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from flask import request, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, login_required, current_user

"""----------   import models module -------"""
from authentication.database.model import Users
from authentication.database.extensions import db
from authentication.database.extensions import OTP, session

from uconra.j_wt import JWT
from uconra.register import Register

from config import Config


jwt_reset_password_bp = Blueprint('jwt_reset_password', __name__,
                                  template_folder='templates',
                                  static_folder='static',
                                  static_url_path='/login/static',
                                  )


@jwt_reset_password_bp.route('/jwt-reset-password', methods=['GET', 'POST'])
def jwt_reset_password():
    # Get user's new password, and confirm password from the user input from the form
    new_password = str(request.form.get('new_password', False))
    confirm_new_password = str(request.form.get('confirm_new_password', False))
    data = request.form.get('data', False)

    if request.method == 'POST':

        if new_password == confirm_new_password:
            hash_password = Register()
            hashed_password = hash_password.userPassword(str(confirm_new_password))

            user_reset_pw = Users.query.filter_by(email=data).first()
            print('user_reset_pw', user_reset_pw)
            user_reset_pw.password = hashed_password
            db.session.commit()
            flash('Password changed successfully. ')
            return redirect(url_for('login.login', ))

        else:
            print('Password do not match. Enter matching passwords')
            flash('Password do not match. Enter matching passwords')

    return render_template('jwt_reset_password.html')


