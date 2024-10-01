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

otp_confirm_bp = Blueprint('confirm', __name__,
                           template_folder='templates',
                           static_folder='/login/static',
                           )

@otp_confirm_bp.route('/otp-confirm', methods=['GET', 'POST'])

def otp_confirm():
    if request.method == 'POST':
        user_input_otp = request.form.get('otp_confirm', False)
        otp_in_db = Users.query.filter_by(otp=user_input_otp).first()

        if not otp_in_db:
            flash('Invalid OTP code')
            print('Invalid OTP code')
            print('Your OTP is: ', OTP)
        elif otp_in_db:
            print('Your OTP is: ', OTP)

            if 'username' in session:
                username = session['username']
                is_username_in_db = Users.query.filter_by(username=username).first()
                if is_username_in_db.confirmed == True:
                    flash('Your are already confirmed')
                    print('You are already confirmed')
                    return redirect(url_for('fruutty_token.index', username=username))
                else:
                    is_username_in_db.confirmed = True
                    is_username_in_db.confirmed_at = func.now()
                    db.session.commit()

                    flash('Account successfully confirmed, \n please login with your credentials.')
                    return redirect(url_for('fruutty_token.index', username=username))

            elif 'get_username_from_login' in session:
                username = session['get_username_from_login']
                is_username_in_db = Users.query.filter_by(username=username).first()
                if is_username_in_db.confirmed == True:
                    flash('Your are already confirmed')
                    print('You are already confirmed')
                    return redirect(url_for('fruutty_token.index', username=username))
                else:
                    is_username_in_db.confirmed = True
                    is_username_in_db.confirmed_at = func.now()


                    flash('Account successfully confirmed, \n please login with your credentials.')
                    return redirect(url_for('fruutty_token.index', username=username))


    return render_template('otp_confirm.html')
