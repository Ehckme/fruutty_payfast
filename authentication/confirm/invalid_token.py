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

from uconra.smtp_mail import SMTP_Mail

from uconra.register import Register

from uconra.email_message import MailMessage

from uconra.j_wt import JWT

from config import Config

invalid_token_bp = Blueprint('invalid_token', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='/login/static',
                            )


@invalid_token_bp.route('/invalid-token', methods=['GET', 'POST'])
def invalid_token():
    user_email = str(request.form.get('email', ))
    print('user email ', user_email)
    valid_email = Register()
    if request.method == 'POST':
        token = JWT()
        email = valid_email.userEmail(user_email)
        print('email ', email)
        is_email_in_db = Users.query.filter_by(email=email).first()
        if is_email_in_db:
            user_token = token.generate_jwt_token(email, key=Config.FLASK_SECRET_KEY)
            username = is_email_in_db.username
            confirm_message = MailMessage()
            sendMail = SMTP_Mail(
                appKey=Config.APP_PASSWORD, userMail=email,
                senderMail=Config.UCONRA_EMAIL, serverEhlo=Config.SERVER_EHLO,
                smtpServer=Config.SMTP_EMAIL_SERVER,
                subject='CONFIRM EMAIL', userName=username,
                message=confirm_message.confirm_message(token=user_token, otp=OTP),
            )
            sendMail.sendMail()
            return redirect(url_for('confirm.otp_confirm'))
        else:
            flash('invalid email')
            return redirect(url_for('email_confirm.email_confirm'))
    return render_template('invalid_token.html')