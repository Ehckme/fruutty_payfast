import requests
from flask import Flask
from flask import flash
from flask import Blueprint
from flask import request, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required
from authentication.database.extensions import session, OTP, db
from authentication.database.model import (Users, Employees,
                                           Employee_login, Employee_address,
                                           Applications
                                           )

from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment


from sqlalchemy import select
from functools import wraps
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from uconra.email_message import MailMessage
from uconra.smtp_mail import SMTP_Mail
from uconra.register import Register
from uconra.j_wt import JWT

from uconra.register import random_chars

from config import Config

"""-----------  import modules for regular expressions  -----------"""
import re

login_bp = Blueprint('login', __name__,
                     template_folder='templates',
                     static_folder='static',
                     static_url_path='/login/static',
                     )

"""---------    Route for login Blueprint   ----------"""



@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    print(request.form)

    # Get user email and password from the user input from the form
    mail = str(request.form.get('email'))
    password = str(request.form.get('password'))

    session['confirm_email'] = request.form.get('email', False)

    register = Register()
    # assign a token variable
    token = JWT()
    # Generate a user token
    user_token = token.generate_jwt_token(mail, key=Config.FLASK_SECRET_KEY)

    password_gen_1 = random_chars(1)
    password_gen_4 = random_chars(4)



    if request.method == 'POST':
        print(request.form)
        recaptcha_secret_response = request.form['g-recaptcha-response']
        recaptcha_verify_response = requests.post(url=f'{Config.GOOGLE_RECAPTCHA_VERIFY_URL}?secret={Config.GOOGLE_RECAPTCHA_SECRETE_KEY}&response={recaptcha_secret_response}').json()
        print(recaptcha_verify_response)

        def create_assessment(
                project_id: str, recaptcha_key: str, token: str, recaptcha_action: str
        ) -> Assessment:
            """Create an assessment to analyze the risk of a UI action.
            Args:
                project_id: Your Google Cloud Project ID.
                recaptcha_key: The reCAPTCHA key associated with the site/app
                token: The generated token obtained from the client.
                recaptcha_action: Action name corresponding to the token.
            """

            client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

            # Set the properties of the event to be tracked.
            event = recaptchaenterprise_v1.Event()
            event.site_key = recaptcha_key
            event.token = token

            assessment = recaptchaenterprise_v1.Assessment()
            assessment.event = event

            project_name = f"projects/{project_id}"

            # Build the assessment request.
            request = recaptchaenterprise_v1.CreateAssessmentRequest()
            request.assessment = assessment
            request.parent = project_name

            response = client.create_assessment(request)

            # Check if the token is valid.
            if not response.token_properties.valid:
                print(
                    "The CreateAssessment call failed because the token was "
                    + "invalid for the following reasons: "
                    + str(response.token_properties.invalid_reason)
                )
                return

            # Check if the expected action was executed.
            if response.token_properties.action != recaptcha_action:
                print(
                    "The action attribute in your reCAPTCHA tag does"
                    + "not match the action you are expecting to score"
                )
                return
            else:
                # Get the risk score and the reason(s).
                # For more information on interpreting the assessment, see:
                # https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
                for reason in response.risk_analysis.reasons:
                    print(reason)
                print(
                    "The reCAPTCHA score for this token is: "
                    + str(response.risk_analysis.score)
                )
                # Get the assessment name (id). Use this to annotate the assessment.
                assessment_name = client.parse_assessment_path(response.name).get("assessment")
                print(f"Assessment name: {assessment_name}")
            return response





        # check email with regular expressions and display flash message
        if re.match(r"\S[^@]+\S+@[^@]+\S+[a-zA-Z]+\S+\.[^@]", mail):
            pass
        else:
            flash('invalid email')

        # Validate the database email with the user input email
        valid_user_email = Users.query.filter_by(email=mail).first()

        if valid_user_email:



            # instantiate PasswordHasher from argon2-cffi
            ph = PasswordHasher()
            hash = valid_user_email.password

            # Use the try block to catch the exception
            try:

                # Verify the hash in database with the user input password
                if ph.verify(hash, password):

                    if ph.check_needs_rehash(hash):
                        valid_user_email.password(valid_user_email, ph.hash(password))

                    # Check if user has confirmed email in database
                    is_confirmed = valid_user_email.confirmed

                    if is_confirmed == True:
                        if valid_user_email.role == 'admin':
                            session['admin_session'] = valid_user_email.user_id
                            # Login the user
                            login_user(valid_user_email)

                            valid_user_email.lastLogin_at = func.now()
                            db.session.commit()

                            # Display flash message
                            flash(f'You are logged in {valid_user_email.username}')
                            print(is_confirmed)
                            return redirect(url_for('employees.admin', id=valid_user_email.id,
                                                    email=valid_user_email.email, role=valid_user_email.role,
                                                    google_recaptcha_site_key=Config.GOOGLE_RECAPTCHA_SITE_KEY,
                                                    ))
                        elif valid_user_email.role == 'rep':
                            session['employee_session'] = valid_user_email.user_id
                            # Login the user
                            login_user(valid_user_email)

                            valid_user_email.lastLogin_at = func.now()
                            db.session.commit()

                            # Display flash message
                            flash(f'You are logged in {valid_user_email.username}')
                            print(is_confirmed)
                            return redirect(url_for('employees.employees',
                                                    id=valid_user_email.id,
                                                    email=valid_user_email.email,
                                                    role=valid_user_email.role,
                                                    google_recaptcha_site_key=Config.GOOGLE_RECAPTCHA_SITE_KEY,
                                                    ))

                        # Login the user
                        login_user(valid_user_email)

                        # user_id = str(current_user.id) + '-' + password_gen_4 + '-' + password_gen_1
                        valid_user_email.lastLogin_at = func.now()
                        db.session.commit()

                        # Display flash message
                        flash(f'You are logged in {valid_user_email.username}')
                        print(is_confirmed)
                        return redirect(url_for('fruutty_token.scanner', google_recaptcha_site_key=Config.GOOGLE_RECAPTCHA_SITE_KEY))  # user_username=valid_user_email.username
                    else:
                        email = register.userEmail(mail)
                        """ -------- Create email message ---------- """
                        confirm_message = MailMessage()
                        sendMail = SMTP_Mail(
                            appKey=Config.APP_PASSWORD, userMail=email,
                            senderMail=Config.MARXZI_EMAIL, serverEhlo=Config.SERVER_EHLO,
                            smtpServer=Config.SMTP_EMAIL_SERVER,
                            subject='CONFIRM EMAIL', userName=valid_user_email.username,
                            message=confirm_message.confirm_message(token=user_token, otp=OTP),
                        )
                        """ -------- Send email ---------- """
                        sendMail.sendMail()

                        flash('To start using our services, please confirm your email account with us! ')
                        return redirect(url_for('confirm.otp_confirm'))
            except VerifyMismatchError:

                # Display a flash message
                print('please enter correct password')
                flash('please enter correct password')
                return redirect(url_for('fruutty_token.index', google_recaptcha_site_key=Config.GOOGLE_RECAPTCHA_SITE_KEY))
        else:

            # Display a flash message
            print('please enter correct email')
            flash('please enter correct email')
            return render_template('index.html', google_recaptcha_site_key=Config.GOOGLE_RECAPTCHA_SITE_KEY)


        pass



    return render_template('login.html', google_recaptcha_site_key=Config.GOOGLE_RECAPTCHA_SITE_KEY)
