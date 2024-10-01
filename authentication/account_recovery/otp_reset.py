from flask import Blueprint
from flask import flash
from flask import request, render_template, url_for, redirect
"""############ import models  #############"""
from authentication.database.model import Users
from authentication.database.extensions import db
from authentication.database.extensions import OTP, session
from uconra.j_wt import JWT
from uconra.register import Register
import json

otp_reset_bp = Blueprint('otp_reset', __name__,
                         template_folder='templates',
                         static_folder='static',
                         static_url_path='/login/static'
                         )


@otp_reset_bp.route('/otp-reset', methods=['GET', 'POST'])
def otp_reset():
    session_browser = request.headers.get('Sec-Ch-Ua')
    session_platform = request.headers.get('Sec-Ch-Ua-Platform')
    session_host = request.headers.get('Host')
    print('Browser: ', session_browser)
    print('Platform: ', session_platform)
    print('Host: ', session_host)
    print('OTP Hash', )
    # print(request.headers)
    if request.method == 'POST':
        user_input_otp = request.form.get('otp_reset', False)
        register = Register()

        if 'user_from_email' in session: #user_input_otp != OTP:
            user_email = session['user_from_email']
            user_email_in_db = Users.query.filter_by(email=user_email).first()
            user_email_otp = str(user_email_in_db.otp)
            if 'reset_otp' in session:
                reset_otp = session['reset_otp']
                if user_input_otp != user_email_otp:
                    print('user email otp in db', user_email_otp)
                    print('Invalid OTP code')
                    flash('Invalid OTP code')
                elif user_input_otp == user_email_otp:
                    print('Your OTP is: ', user_email_otp)
                    flash('Email confirmed.')
                    return redirect(url_for('reset_password.reset_password' ))

    flash('To varify it is you?! ')
    return render_template('otp_reset.html')