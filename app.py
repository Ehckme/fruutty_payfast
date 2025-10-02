import fileinput

import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from flask import Flask
from flask import flash
from flask import Blueprint
from flask import request, render_template, redirect, url_for

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask_admin import helpers, expose

''' ####################  import flask-login #########################'''
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from authentication.logout.logout import logout_bp

''' ####################  import fruutty token Blueprints #########################'''

from fruutty_token.fruutty_token import fruutty_token_bp
from fruutty_player.fruutty_player import fruuty_player_bp

''' ####################  import PayFast  Blueprints #########################'''

from payfast.token_sales import payfast_bp

''' ####################  import Employees Blueprints #########################'''
from employees.employees import employees_bp

''' ####################  import documentation  Blueprints #########################'''
from documentation.fruutty_docs import documentation_bp

''' ####################  import authentication Blueprints #########################'''
from authentication.login.login import login_bp
from authentication.sign_up.sign_up import sign_up_pb
from authentication.confirm.jwt_confirm import jwt_confirm_bp
from authentication.confirm.otp_confirm import otp_confirm_bp
from authentication.account_recovery.account_recovery import account_recovery_bp
from authentication.account_recovery.jwt_reset import jwt_reset_bp
from authentication.account_recovery.otp_reset import otp_reset_bp
from authentication.confirm.resend_token import resend_token_bp
from authentication.confirm.email_confirm import email_confirm_bp
from authentication.confirm.invalid_token import invalid_token_bp
from authentication.confirm.account_active import account_active_bp
from authentication.confirm.invalidReset_token import invalidReset_token_bp
from authentication.confirm.emailReset_confirm import emailReset_confirm_bp
from authentication.confirm.resendReset_token import resendReset_token_bp
from authentication.account_recovery.reset_password import reset_password_bp
from authentication.account_recovery.jwt_reset_password import jwt_reset_password_bp
from terms_and_conditions.terms_and_conditions import terms_and_conditions_bp
from dashboard.dashboard import dashboard_bp
from authentication.database.extensions import db, OTP, session
from authentication.database.model import (
    Users, Music, Food, Drive, Tech, Fashion, Employee_login, Sales

                                           )
# UCONRA
from uconra.register import random_chars

from config import Config

"""
File uploads import section
"""

import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

from flask_migrate import Migrate

UPLOAD_FOLDER = 'fruutty_token/static/img/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'wav', 'mp3'}


app = Flask(__name__)

"""
6LfY3S0qAAAAAEkbrbBFA2vIFzFrt81n3efZK5d0

recaptcha API key = AIzaSyA8Ug2xQjnaxQKR6CTGjHcGq5xVKZ12pKs

Config settings
"""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SECRET_KEY'] = 'the random string'
""" --------    Create a connection to the database using mysql and + pymysql   -----------"""
app.config['SQLALCHEMY_DATABASE_URI'] = Config.UCONRA_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = {'auth_roles' : 'mysql+pymysql://root:#FruuttydbPassword123@localhost/Fruutty_employees'}
"""-----------  config secrete key  ---------"""
app.config['SECRET_KEY'] = Config.FLASK_SECRET_KEY
"""-----------  config google recaptcha secrete key  ---------"""

"""

recaptcha site = 6LdcQy4qAAAAANL4BY2fWNINYF7UKN7_pdhVrGOH

recaptcha secrete = 6LdcQy4qAAAAAIXDD3NXNimTPpqnKTUzRQC-QaGR

"""


app.config['GOOGLE_RECAPTCHA_SITE_KEY'] = Config.GOOGLE_RECAPTCHA_SITE_KEY
app.config['GOOGLE_RECAPTCHA_SECRETE_KEY'] = Config.GOOGLE_RECAPTCHA_SECRETE_KEY
app.config['GOOGLE_RECAPTCHA_VERIFY_URL'] = Config.GOOGLE_RECAPTCHA_VERIFY_URL

"""-----------  initialize flask-migrate  ---------"""
migrate = Migrate(app, db)

"""-----------  initialize database app  ---------"""
db.init_app(app)
db.app = app
app.app_context().push()

"""
Fruutty Token Blueprint section
"""
app.register_blueprint(fruutty_token_bp)
app.register_blueprint(fruuty_player_bp)

"""----------  PayFast  Blueprints Section -------"""

app.register_blueprint(payfast_bp, url_prefix="/payfast")

"""----------  fruutty_docs  Blueprints Section -------"""

app.register_blueprint(documentation_bp, url_prefix="/documentation")

"""----------  Employee Blueprints Section -------"""
app.register_blueprint(employees_bp)

"""----------  Authentication Blueprints Section -------"""
app.register_blueprint(login_bp)
app.register_blueprint(sign_up_pb)
app.register_blueprint(jwt_confirm_bp)
app.register_blueprint(otp_confirm_bp)
app.register_blueprint(account_recovery_bp)
app.register_blueprint(jwt_reset_bp)
app.register_blueprint(otp_reset_bp)
app.register_blueprint(resend_token_bp)
app.register_blueprint(email_confirm_bp)
app.register_blueprint(invalid_token_bp)
app.register_blueprint(account_active_bp)
app.register_blueprint(invalidReset_token_bp)
app.register_blueprint(emailReset_confirm_bp)
app.register_blueprint(reset_password_bp)
app.register_blueprint(jwt_reset_password_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(terms_and_conditions_bp)
app.register_blueprint(logout_bp)


"""
main app config routes section
"""
"""
Hamdle 404 errors and return index html for login
"""



@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/music-upload/<int:id>/<email>/<role>', methods=['GET', 'POST'])
def music_upload(id, email, role):
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')


    record_company = request.form.get('record_company', False)
    image_link = request.form.get('image_link', False)
    song_link = request.form.get('song_link', False)
    song_name = request.form.get('song_name', False)
    artist_name = request.form.get( 'artist_name', False)
    artist_bio = request.form.get('artist_bio', False)
    lyrics = request.form.get('lyrics', False)

    data = [{'discount': 'none'},
            {'discount': '5%'}, {'discount': '10%'},
            {'discount': '15%'}, {'discount': '20%'},
            {'discount': '25%'}, {'discount': '30%'},
            {'discount': '35%'}, {'discount': '40%'},
            {'discount': '45%'}, {'discount': '50%'}]
    select_discount = request.form.get('discount', False)

    if request.method == 'POST':
        try:
            amount = int(request.form.get('amount', False))
            if amount == '':
                flash('enter amount')
                return redirect((request.url))
        except ValueError:
            flash('enter amounnt value')
            return redirect((request.url))
        if record_company == '':
            flash('enter company name')
            return redirect((request.url))
        if image_link == '':
            flash('enter image link')
            return redirect((request.url))
        if song_name == '':
            flash('enter song name')
            return redirect((request.url))
        if artist_name == '':
            flash('enter artist name')
            return redirect((request.url))
        if artist_bio == '':
            flash('enter artist bio')
            return redirect((request.url))
        if lyrics == '':
            flash('enter lyrics')
            return redirect((request.url))

        if record_company == '' and link == '':
            flash('enter all values')
            return redirect((request.url))
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect((request.url))
        file_to_upload = request.files['file']
        # if the usr does not select a file, the browser submits an
        # empty file without a filename.

        if file_to_upload.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file_to_upload and allowed_file(file_to_upload.filename):
            filename = secure_filename(file_to_upload.filename)

            music_file = Music(
                employee_id=current_user.user_id,
                audio_file_name=filename,
                song_name=song_name,
                artist_name=artist_name,
                artist_bio=artist_bio,
                record_company=record_company,
                image_link=image_link,
                song_link=song_link,
                lyrics=lyrics,

            )

            value_to_discount = (amount * int(select_discount.rstrip("%"))) / 100
            discount = amount - value_to_discount

            paid_sales = Sales(
                employee_id=current_user.user_id,
                upload_section='food_upload',
                company=record_company,
                amount=amount,
                discount=discount,
                date=func.now(),
            )
            db.session.add(music_file)
            db.session.add(paid_sales)
            db.session.commit()

            file_to_upload.save(os.path.join(app.config['UPLOAD_FOLDER'] + 'music', filename))
            return render_template('message.html')
    return render_template('music_upload.html',
                           id=current_user.id,
                           email=current_user.email,
                           role=current_user.role,
                           data=data,
                           )


@app.route('/fruutty_token/static/img/music/<name>')
def download_music(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + 'music', name)


"""
food upload route section
"""


@app.route('/food-upload/<int:id>/<email>/<role>', methods=['GET', 'POST'])
def food_upload(id, email, role):
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')


    company_name = request.form.get('company_name', False)
    link = request.form.get('link', False)


    data = [{'discount': 'none'},
            {'discount': '5%'}, {'discount': '10%'},
            {'discount': '15%'}, {'discount': '20%'},
            {'discount': '25%'}, {'discount': '30%'},
            {'discount': '35%'}, {'discount': '40%'},
            {'discount': '45%'}, {'discount': '50%'}     ]
    select_discount = request.form.get('discount', False)

    if request.method == 'POST':
        try:
            amount = int(request.form.get('amount', False))
            if amount == '':
                flash('enter amount')
                return redirect((request.url))
        except ValueError:
            flash('enter amounnt value')
            return redirect((request.url))
        if company_name == '':
            flash('enter company name')
            return redirect((request.url))
        if link == '':
            flash('enter link')
            return redirect((request.url))

        if company_name == '' and link == '':
            flash('enter all values')
            return redirect((request.url))

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect((request.url))
        file_to_upload = request.files['file']
        # if the usr does not select a file, the browser submits an
        # empty file without a filename.

        if file_to_upload.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file_to_upload and allowed_file(file_to_upload.filename):
            filename = secure_filename(file_to_upload.filename)
            food_image = Food(
                employee_id=current_user.user_id,
                image_name=filename,
                company_name=company_name,
                link=link,

            )
            value_to_discount = (amount * int(select_discount.rstrip("%"))) / 100
            discount = amount - value_to_discount

            paid_sales = Sales(
                employee_id=current_user.user_id,
                upload_section='food_upload',
                company=company_name,
                amount=amount,
                discount=discount,
                date=func.now(),
            )

            db.session.add(food_image)
            db.session.add(paid_sales)
            db.session.commit()
            file_to_upload.save(os.path.join(app.config['UPLOAD_FOLDER'] + 'food', filename))
            message = 'Uploaded Successfully'
            flash(message)

            return redirect(url_for('download_food', name=filename))

    return render_template('food_upload.html',
                           id=current_user.id,
                           email=current_user.email,
                           role=current_user.role,
                           data=data,
                           )


@app.route('/fruutty_token/static/img/food/<name>')
def download_food(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + 'food', name)


"""
fashion upload route section
"""


@app.route('/fashion-upload/<int:id>/<email>/<role>', methods=['GET', 'POST'])
def fashion_upload(id, email, role):
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')

    company_name = request.form.get('company_name', False)
    link = request.form.get('link', False)


    data = [{'discount': 'none'},
            {'discount': '5%'}, {'discount': '10%'},
            {'discount': '15%'}, {'discount': '20%'},
            {'discount': '25%'}, {'discount': '30%'},
            {'discount': '35%'}, {'discount': '40%'},
            {'discount': '45%'}, {'discount': '50%'}]
    select_discount = request.form.get('discount', False)

    if request.method == 'POST':
        try:
            amount = int(request.form.get('amount', False))
            if amount == '':
                flash('enter amount')
                return redirect((request.url))
        except ValueError:
            flash('enter amounnt value')
            return redirect((request.url))
        if company_name == '':
            flash('enter company name')
            return redirect((request.url))
        if link == '':
            flash('enter link')
            return redirect((request.url))
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect((request.url))
        file_to_upload = request.files['file']
        # if the usr does not select a file, the browser submits an
        # empty file without a filename.

        if file_to_upload.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file_to_upload and allowed_file(file_to_upload.filename):
            filename = secure_filename(file_to_upload.filename)
            fashion_image = Fashion(
                employee_id=random_chars(8),
                image_name=filename,
                company_name=company_name,
                link=link,

            )
            value_to_discount = (amount * int(select_discount.rstrip("%"))) / 100
            discount = amount - value_to_discount
            paid_sales = Sales(
                employee_id=current_user.user_id,
                upload_section='fashion_upload',
                company=company_name,
                amount=amount,
                discount=discount,
                date=func.now(),
            )
            db.session.add(fashion_image)
            db.session.add(paid_sales)
            db.session.commit()
            file_to_upload.save(os.path.join(app.config['UPLOAD_FOLDER'] + 'fashion', filename))
            return redirect(url_for('download_fashion', name=filename))
    return render_template('fashion_upload.html',
                           id=current_user.id,
                           email=current_user.email,
                           role=current_user.role,
                           data=data,
                           )


@app.route('/fruutty_token/static/img/fashion/<name>')
def download_fashion(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + 'fashion', name)


"""
drive upload route section
"""


@app.route('/drive-upload/<int:id>/<email>/<role>', methods=['GET', 'POST'])
def drive_upload(id, email, role):
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')

    company_name = request.form.get('company_name', False)
    link = request.form.get('link', False)



    data = [{'discount': 'none'},
            {'discount': '5%'}, {'discount': '10%'},
            {'discount': '15%'}, {'discount': '20%'},
            {'discount': '25%'}, {'discount': '30%'},
            {'discount': '35%'}, {'discount': '40%'},
            {'discount': '45%'}, {'discount': '50%'}]
    select_discount = request.form.get('discount', False)

    if request.method == 'POST':
        try:
            amount = int(request.form.get('amount', False))
            if amount == '':
                flash('enter amount')
                return redirect((request.url))
        except ValueError:
            flash('enter amounnt value')
            return redirect((request.url))
        if company_name == '':
            flash('enter company name')
            return redirect((request.url))
        if link == '':
            flash('enter link')
            return redirect((request.url))
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect((request.url))
        file_to_upload = request.files['file']
        # if the usr does not select a file, the browser submits an
        # empty file without a filename.

        if file_to_upload.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file_to_upload and allowed_file(file_to_upload.filename):
            filename = secure_filename(file_to_upload.filename)
            drive_image = Drive(
                employee_id=current_user.user_id,
                image_name=filename,
                company_name=company_name,
                link=link,

            )

            value_to_discount = (amount * int(select_discount.rstrip("%"))) / 100
            discount = amount - value_to_discount
            paid_sales = Sales(
                employee_id=current_user.user_id,
                upload_section='drive_upload',
                company=company_name,
                amount=amount,
                discount=discount,
                date=func.now(),
            )
            db.session.add(drive_image)
            db.session.add(paid_sales)
            db.session.commit()
            file_to_upload.save(os.path.join(app.config['UPLOAD_FOLDER'] + 'drive', filename))
            return redirect(url_for('download_drive', name=filename))
    return render_template('drive_upload.html',
                           id=current_user.id,
                           email=current_user.email,
                           role=current_user.role,
                           data=data,

                           )


@app.route('/fruutty_token/static/img/drive/<name>')
def download_drive(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + 'drive', name)


"""
drive upload route section
"""


@app.route('/smart-tech-upload/<int:id>/<email>/<role>', methods=['GET', 'POST'])
def smart_tech_upload(id, email, role):
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')

    company_name = request.form.get('company_name', False)
    link = request.form.get('link', False)

    data = [{'discount': 'none'},
            {'discount': '5%'}, {'discount': '10%'},
            {'discount': '15%'}, {'discount': '20%'},
            {'discount': '25%'}, {'discount': '30%'},
            {'discount': '35%'}, {'discount': '40%'},
            {'discount': '45%'}, {'discount': '50%'}]
    select_discount = request.form.get('discount', False)

    if request.method == 'POST':
        try:
            amount = int(request.form.get('amount', False))
            if amount == '':
                flash('enter amount')
                return redirect((request.url))
        except ValueError:
            flash('enter amounnt value')
            return redirect((request.url))
        if company_name == '':
            flash('enter company name')
            return redirect((request.url))
        if link == '':
            flash('enter link')
            return redirect((request.url))
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect((request.url))
        file_to_upload = request.files['file']
        # if the usr does not select a file, the browser submits an
        # empty file without a filename.

        if file_to_upload.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file_to_upload and allowed_file(file_to_upload.filename):
            filename = secure_filename(file_to_upload.filename)

            tech_image = Tech(
                employee_id=random_chars(8),
                image_name=filename,
                company_name=company_name,
                link=link,

            )

            value_to_discount = (amount * int(select_discount.rstrip("%"))) / 100
            discount = amount - value_to_discount

            paid_sales = Sales(
                employee_id=current_user.user_id,
                upload_section='smart_tech_upload',
                company=company_name,
                amount=amount,
                discount=discount,
                date=func.now(),
            )
            db.session.add(tech_image)
            db.session.add(paid_sales)
            db.session.commit()
            file_to_upload.save(os.path.join(app.config['UPLOAD_FOLDER'] + 'smart_tech', filename))
            return redirect(url_for('download_smart_tech', name=filename))
    return render_template('smart_tech_upload.html',
                           id=current_user.id,
                           email=current_user.email,
                           role=current_user.role,
                           data=data,

                           )


@app.route('/fruutty_token/static/img/smart_tech/<name>')
def download_smart_tech(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + 'smart_tech', name)

"""--------------   create the application object   ----------------"""

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'

''' ##########  Load user from login_manager with their user id. ###########'''

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Users, int(user_id))

with app.app_context():
    db.create_all()
    db.create_all(bind_key=["auth_roles"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
