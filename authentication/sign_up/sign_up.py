"""############ import flask and all necessary modules #############"""
from flask import Flask
from flask import flash
from flask import Blueprint
from flask import request, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, current_user
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

# importing geopy library
from geopy.geocoders import Nominatim
# import requests and json
from requests import get
import json

# password_gen
from uconra.register import random_chars

""" -------- Create a stand alone Blueprint for sign_up---------- """
sign_up_pb = Blueprint('sign_up', __name__,
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='/login/static/'
                       )
""" -------- Create a route to the Blueprint ---------- """
@sign_up_pb.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # Get user email, username and password from the user input from the form
    register = Register()
    password_gen = random_chars(8)

    user_email = str(request.form.get('email'))
    user_name = request.form.get('username')
    pass_word = str(request.form.get('password'))

    # get user location from url requests library
    url = 'http://ipinfo.io/json'
    response = get(url)
    data = json.loads(response.text)
    country = data['country']

    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")

    # get the location name
    getLoc = loc.geocode(f"{country}")



    # create a session containing the user's username
    session['username'] = request.form.get('username')

    if request.method == 'POST':
        email = str(register.userEmail(user_email))
        username = user_name
        password = register.userPassword(pass_word)
        email_in_database = Users.query.filter_by(email=email).first()


        # assign a token variable
        token = JWT()
        # Generate a user token
        user_token = token.generate_jwt_token(email, key=Config.FLASK_SECRET_KEY)
        link = 'http://0.0.0.0:5000/jwt-confirm/' + user_token

        # check email
        if not email:
            message = 'incorrect email input'
            print(message)
        else:
            if email_in_database and email_in_database.confirmed == True:
                message = 'email already exists'
                print(message)
                flash(message=message)
                return redirect(url_for('account_active.account_active'))
            elif email_in_database:
                message = 'email already exists'
                print(message)
                flash(message=message)
                return redirect(url_for('sign_up.sign_up'))
            else:
                try:
                    """ -------- Create email message ---------- """
                    confirm_message = MailMessage()
                    sendMail = SMTP_Mail(
                        appKey=Config.APP_PASSWORD, userMail=email,
                        senderMail=Config.UCONRA_EMAIL, serverEhlo=Config.SERVER_EHLO,
                        smtpServer=Config.SMTP_EMAIL_SERVER,
                        subject='CONFIRM EMAIL', userName=username,
                        message=confirm_message.confirm_message(token=user_token, otp=OTP),
                    )
                    """ -------- Send email ---------- """
                    sendMail.sendMail()
                    new_user = Users(
                        user_id=password_gen,
                        email=email,
                        username=username,
                        password=password,
                        otp=OTP,
                        country=getLoc.address,
                    )
                    db.session.add(new_user)
                    db.session.commit()
                    print('Commited to database')
                    return redirect(url_for('confirm.otp_confirm'))

                except:
                    print('Mail Error 1')
                    flash('incorrect email input')
                    return redirect(url_for('fruutty_token.index'))


    return render_template('sign_up.html')


