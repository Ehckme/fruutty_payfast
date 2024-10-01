"""############ import flask and all necessary modules #############"""
from flask import Flask
from flask import flash
from flask import make_response
import json
from flask import Blueprint
from flask import request, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager
"""############ import models  #############"""
from authentication.database.model import Users
from authentication.database.extensions import db
from authentication.database.extensions import OTP, session
"""############ import Register and SMTP_MAIL from uconra #############"""
from uconra.register import Register
from uconra.smtp_mail import SMTP_Mail
"""############ import Config settings #############"""
from config import Config
"""############ import MailMessage from email_message #############"""
from uconra.email_message import MailMessage
from uconra.j_wt import JWT

account_recovery_bp = Blueprint('account_recovery', __name__,
                                template_folder='templates',
                                static_folder='static',
                                static_url_path='/login/static'
                                )

"""---------    Route for account_recovery Blueprint   ----------"""

@account_recovery_bp.route('/account-recovery', methods=['GET', 'POST'])
def account_recovery():
    register = Register()
    email_to_recover = str(request.form.get('email'))
    check_recovery_email = Users.query.filter_by(email=email_to_recover).first()


    if request.method == 'POST':
        # create a session containing the user's username from email
        session['user_from_email'] = check_recovery_email.email


        if check_recovery_email:
            email = register.userEmail(email_to_recover)
            confirm_message = MailMessage()

            # assign a token variable
            token = JWT()
            # Generate a user token
            user_token = token.generate_jwt_token(email, key=Config.FLASK_SECRET_KEY)

            check_recovery_email.otp = OTP
            db.session.commit()
            session['reset_otp'] = check_recovery_email.otp
            print('session["reset_otp"] = ', check_recovery_email.otp)
            sendMail = SMTP_Mail(
                appKey=Config.APP_PASSWORD, userMail=email,
                senderMail=Config.UCONRA_EMAIL, serverEhlo=Config.SERVER_EHLO,
                smtpServer=Config.SMTP_EMAIL_SERVER,
                subject='RESET PASSWORD', userName=check_recovery_email.username,
                message=confirm_message.reset_message( otp=check_recovery_email.otp),
            ) # token=user_token
            sendMail.sendMail()
            json_otp = f'{{"OTP": {OTP}}}'
            jsonLoads_otp = json.loads(json_otp)
            print(jsonLoads_otp['OTP'])
            load = str(jsonLoads_otp['OTP'])
            otp_hash = register.hash_encryption(OTP)
            # redirect(url_for('otp_reset.otp_reset', otp=otp_hash))
            return redirect(url_for('otp_reset.otp_reset', otp=otp_hash))

    return render_template('account_recovery.html')