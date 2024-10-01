from flask import Flask
from flask import flash
from flask import Blueprint
from flask import request, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required
from fruutty_token.create_token import Token
from uconra.register import random_chars
from authentication.database.model import (Users, Fruutty_transactions,
                                           Fruutty_token, Ftvs,
                                           Sent_tokens, Received_tokens,
                                           Notifications, Food,
                                           Fashion, Drive,
                                           Tech, Music, Employee_login, Admin_token_request,
                                           )
from sqlalchemy import select
from functools import wraps
from sqlalchemy import DateTime
from sqlalchemy.sql import func

import uconra


from authentication.database.extensions import db
from authentication.database.extensions import OTP, session

from currencie.currency_pair import Currency_Pairs
# import countries from trading_countres
from trading_countries import countries

import json
# importing geopy library & requests
from geopy.geocoders import Nominatim
from requests import get

import io
import base64
from PIL import Image
from config import Config

from collections import  defaultdict

fruutty_token_bp = Blueprint('fruutty_token', __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='/static/fruutty_token',
                             )

"""
##############################################
Section for aquiring and setting user location
##############################################
"""
# get user location from url requests library
url = 'http://ipinfo.io/json'
response = get(url)
data = json.loads(response.text)
city = data['city']
country = data['country']
SOUTH_AFRICA = 'South Africa'
UNITED_STATES = 'United States'

# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")
# get the location name
getLoc = loc.geocode(f"{country}")
getloc_country = getLoc.address


def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'confirm_email' in session:
            admin_session = session['confirm_email']
            admin_email_in_db = db.session.execute(db.select(Employee_login).order_by(Employee_login.role)).scalars()
            for email in admin_email_in_db:
                admin_role_in_db = email.role
                print(admin_role_in_db)
                admin_role = 'admin'
                if admin_role_in_db != admin_role:
                    return redirect(url_for('login.login', code=302, next=request.url))
                else:
                    return render_template('admin.html')

        return f(*args, **kwargs)
    return decorated_function

def current_user_email():
    email = current_user.email
    return email

@fruutty_token_bp.route('/')
@fruutty_token_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', google_recaptcha_site_key=Config.GOOGLE_RECAPTCHA_SITE_KEY,)


@fruutty_token_bp.route('/fruutty', methods=['GET', 'POST'])
def fruutty():
    return render_template('fruutty.html')


@fruutty_token_bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    rep = 'rep'
    if current_user.role == rep:
        flash('login to access this page')
        return render_template('index.html')
    fruuty_toke_amount = request.form.get('fruutty_token', False)
    # print('current user', current_user.id)
    # print('current user', current_user.email)
    # print('current user', current_user.user_id)

    if request.method == 'POST':
        try:
            token = Token()
            mail = current_user.email
            id = str(current_user.id)
            user_id = current_user.user_id
            token_id = random_chars(4)
            token_type = 'money'
            user_country = current_user.country
            trade_country = getloc_country
            token_name = id + mail
            fruuty_token = token.fruuty_token(
                fruuty_toke_amount,
                name=token_name,
                user_id=user_id,
                token_id=token_id,
                token_type=token_type,
                city=city,
                user_country=user_country,
                trade_country=trade_country,

            )
            print(fruuty_token)

            # What image do we open here
            qr_image = Image.open(f'{token_name}' + '.png')
            data = io.BytesIO()
            qr_image.save(data, 'PNG')
            encoded_qr_image = base64.b64encode(data.getvalue())

            return render_template('generate.html', token=encoded_qr_image.decode('utf-8'))
        except AttributeError:
            message = 'Forbidden Ristriction'
            return message

    return render_template('generate.html')


@fruutty_token_bp.route('/scanner', methods=['GET', 'POST'])
@login_required
def scanner():
    rep = 'rep'
    if current_user.role == rep:
        flash('login to access this page')
        return render_template('index.html')
    if request.method == 'POST':
        data = str(request.form.get('token_results', False))
        email = current_user.email

        global json_response
        try:
            json_response = json.loads(data)
            print('json loads = ', json_response)
            print(json_response['token_id'])
            if json_response['token_type'] == 'money':
                current_user_tokens = current_user.fruutty_token
                current_user.fruutty_token = current_user_tokens + float(json_response['token_amount'])
                db.session.commit()
                # process the user token transaction
                user_transaction = Fruutty_transactions(
                    user_id=current_user.user_id,
                    token_id=json_response['token_id'],
                    token_type=json_response['token_type'],
                    product_name=json_response['product_name'],
                    store_name=json_response['store_name'],
                    token_amount=json_response['token_amount'],
                    from_owner=json_response['user_id'],
                    location=city,
                )
                db.session.add(user_transaction)
                db.session.commit()
            elif json_response['token_type'] == 'product':
                current_user_tokens = current_user.fruutty_token
                current_user.fruutty_token = current_user_tokens - float(json_response['token_amount'])
                db.session.commit()
            flash('token', data)
            return render_template('scanner_results.html',
                                   # store_name=json_response['store_name'],
                                   user=json_response['user_id'],
                                   token_id=json_response['token_id'],
                                   token_type=json_response['token_type'],
                                   product_name=json_response['product_name'],
                                   token_amount=json_response['token_amount'],
                                   city=json_response['city'],
                                   user_countryr=json_response['user_country'],
                                   trade_country=json_response['trade_country'],
                                   date=json_response['date'],
                                   # Processor=json_response['Processor'],

                                   )
        except json.decoder.JSONDecodeError as e:
            flash('OOPS! There seems to be an attempt, looks like you tried to create a token without scanning.')
            return render_template('error.html', )

    return render_template('scanner.html', )

@fruutty_token_bp.route('/send-token', methods=['GET', 'POST'])
@login_required
def send_token():
    rep = 'rep'
    if current_user.role == rep:
        flash('login to access this page')
        return render_template('index.html')
    recieving_email = request.form.get('recieving_email', False)
    token_amount_to_send = request.form.get('token_amount_to_send', False)
    if request.method == 'POST':
        sender_email = current_user.email
        reciever_email = Users.query.filter_by(email=recieving_email).first()

        currency_pair = Currency_Pairs()
        # get the current user location country trading value
        multiplire = countries[f'{getloc_country}']
        # Get the trading value from Ftvs database table
        # trade_value = db.session.execute(db.select(User).order_by(User.username)).scalars()
        trade_value = db.session.execute(db.select(Ftvs).order_by(Ftvs.average)).scalar()
        token_trade_value = trade_value.average

        """
        Admin section to send tokens
        """
        """
        if 'confirm_email' in session:
            admin_email = session['confirm_email']
            admin_email_in_db = Employee_login.query.filter_by(email=admin_email).first()
            
            if admin_email_in_db.e
        """

        if current_user.country == SOUTH_AFRICA and reciever_email.country == UNITED_STATES:
            usa_token_amount = float(token_amount_to_send) * float(multiplire)
            usa_token = usa_token_amount / float(token_trade_value)
            #
            reciever_tokens = float(reciever_email.fruutty_token)
            reciever_email.fruutty_token = reciever_tokens + float(usa_token)
            #
            sent_tokens = Sent_tokens(
                user_id=current_user.user_id,
                token_reference=random_chars(8),
                token_amount=token_amount_to_send,
                token_value=usa_token,
                receiver=recieving_email,
            )
            # recieving tokens
            received_tokens = Received_tokens(
                user_id=current_user.user_id,
                token_reference=random_chars(8),
                token_amount=token_amount_to_send,
                token_value=usa_token,
                sender=current_user.email,
            )
            db.session.add(sent_tokens)
            db.session.add(received_tokens)
            db.session.commit()
            print('SA Token To Send ', sa_token_to_send)

        if current_user.country == UNITED_STATES and reciever_email.country == SOUTH_AFRICA:
            us_to_sa_token_amount = float(token_amount_to_send) / float(multiplire)
            us_to_sa_token = us_to_sa_token_amount / float(token_trade_value)

            reciever_tokens = float(reciever_email.fruutty_token)
            reciever_email.fruutty_token = reciever_tokens + float(us_to_sa_token)

            # sending tokens
            sent_tokens = Sent_tokens(
                user_id=current_user.user_id,
                token_reference=random_chars(8),
                token_amount=token_amount_to_send,
                token_value=us_to_sa_token,
                receiver=recieving_email,
            )
            # recieving tokens
            received_tokens = Received_tokens(
                user_id=current_user.user_id,
                token_reference=random_chars(8),
                token_amount=token_amount_to_send,
                token_value=us_to_sa_token,
                sender=current_user.email,
            )
            db.session.add(sent_tokens)
            db.session.add(received_tokens)
            db.session.commit()
            print('RECIEVER EMAIl ', reciever_email.email)

        elif current_user.country == UNITED_STATES and reciever_email.country == UNITED_STATES:
            usa_to_usa_token_amount = float(token_amount_to_send)  * float(multiplire)
            usa_to_usa_token = usa_to_usa_token_amount / float(token_trade_value)

            reciever_tokens = float(reciever_email.fruutty_token)
            reciever_email.fruutty_token = reciever_tokens + float(usa_to_usa_token)

            # sending tokens
            sent_tokens = Sent_tokens(
                user_id=current_user.user_id,
                token_reference=random_chars(8),
                token_amount=token_amount_to_send,
                token_value=usa_to_usa_token,
                receiver=recieving_email,
            )
            # recieving tokens
            received_tokens = Received_tokens(
                user_id=current_user.user_id,
                token_reference=random_chars(8),
                token_amount=token_amount_to_send,
                token_value=usa_to_usa_token,
                sender=current_user.email,
            )
            db.session.add(sent_tokens)
            db.session.add(received_tokens)
            db.session.commit()
            print('RECIEVER EMAIl ', reciever_email.email)



        if current_user.country == SOUTH_AFRICA and reciever_email.country != SOUTH_AFRICA:
            """
            ##################################################################
            Convert and Exchange foreign token to the equivalent of trade value
            of the South African Rand (ZAR)
            ##################################################################
            """
            foreign_token_amount = float(token_amount_to_send) * float(countries[f'{current_user.country}'])
            forein_token = float(foreign_token_amount) / float(token_trade_value)

            reciever_tokens = float(reciever_email.fruutty_token)
            reciever_email.fruutty_token = reciever_tokens + float(forein_token)

            # sending tokens
            sent_tokens = Sent_tokens(
                user_id=current_user.user_id,
                token_reference=random_chars(8),
                token_amount=token_amount_to_send,
                token_value=forein_token,
                receiver=recieving_email,
            )
            # recieving tokens
            received_tokens = Received_tokens(
                user_id=current_user.user_id,
                token_reference=random_chars(8),
                token_amount=token_amount_to_send,
                token_value=forein_token,
                sender=current_user.email,
            )
            db.session.add(sent_tokens)
            db.session.add(received_tokens)
            db.session.commit()
            print('RECIEVER EMAIl ', reciever_email.email)

        if current_user.country == getloc_country and reciever_email.country == getloc_country:
            if getloc_country == SOUTH_AFRICA:
                """
                ##########################################################
                Convert and Send tokens from South Africa to a 
                South African Recipient
                ##########################################################
                """
                sa_token_to_send = float(token_amount_to_send) / float(token_trade_value)

                reciever_tokens = float(reciever_email.fruutty_token)
                reciever_email.fruutty_token = reciever_tokens + float(sa_token_to_send)

                sent_tokens = Sent_tokens(
                    user_id=current_user.user_id,
                    token_reference=random_chars(8),
                    token_amount=token_amount_to_send,
                    token_value=sa_token_to_send,
                    receiver=recieving_email,
                )
                # recieving tokens
                received_tokens = Received_tokens(
                    user_id=current_user.user_id,
                    token_reference=random_chars(8),
                    token_amount=token_amount_to_send,
                    token_value=sa_token_to_send,
                    sender=current_user.email,
                )
                db.session.add(sent_tokens)
                db.session.add(received_tokens)
                db.session.commit()
                print('SA Token To Send ', sa_token_to_send)

            else:

                """
                Token amount to send divided by that user country trading value
                then multiply by token value
    
                """
                tokens_amount_value = float(token_amount_to_send) / float(countries[f'{getloc_country}'])
                tokens_to_send = tokens_amount_value / float(token_trade_value)

                reciever_tokens = float(reciever_email.fruutty_token)
                reciever_email.fruutty_token = reciever_tokens + float(tokens_to_send)
                """
                send and record tokens into Sent and Recieved tokens tables
                """
                # sending tokens
                sent_tokens = Sent_tokens(
                    user_id=current_user.user_id,
                    token_reference=random_chars(8),
                    token_amount=token_amount_to_send,
                    token_value=tokens_to_send,
                    receiver=recieving_email,
                )
                # recieving tokens
                received_tokens = Received_tokens(
                    user_id=current_user.user_id,
                    token_reference=random_chars(8),
                    token_amount=token_amount_to_send,
                    token_value=tokens_to_send,
                    sender=current_user.email,
                )
                db.session.add(sent_tokens)
                db.session.add(received_tokens)
                db.session.commit()
                print('RECIEVER EMAIl 2 ', reciever_email.email)


        return render_template('token_sent.html')

    return render_template('send_token.html')


@fruutty_token_bp.route('/product-token', methods=['GET', 'POST'])
@login_required
def product_token():
    rep = 'rep'
    if current_user.role == rep:
        flash('login to access this page')
        return render_template('index.html')
    fruuty_toke_amount = request.form.get('fruutty_token', False)
    product_name = request.form.get('product_token', False)


    """
    ##############################################
    Section for aquiring and setting user location
    ##############################################
    """
    # get user location from url requests library
    url = 'http://ipinfo.io/json'
    response = get(url)
    data = json.loads(response.text)
    city = data['city']
    country = data['country']

    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")
    # get the location name
    getLoc = loc.geocode(f"{country}")
    getloc_country = getLoc.address

    if request.method == 'POST':
        print('current user', current_user.id)
        print('current user', current_user.email)

        token = Token()
        mail = current_user.email
        id = str(current_user.id)
        user_id = current_user.user_id
        token_id = random_chars(4)
        produt_token = 'product'
        user_country = current_user.country
        trade_country = getloc_country
        token_name = id + mail
        fruuty_token = token.fruuty_token(
            fruuty_toke_amount,
            name=token_name,
            user_id=user_id,
            token_id=token_id,
            token_type=produt_token,
            product_name=product_name,
            city=city,
            user_country=user_country,
            trade_country=trade_country,

        )
        print(fruuty_token)

        # What image do we open here
        qr_image = Image.open(f'{token_name}' + '.png')
        data = io.BytesIO()
        qr_image.save(data, 'PNG')
        encoded_qr_image = base64.b64encode(data.getvalue())

        return render_template('product_token.html', token=encoded_qr_image.decode('utf-8'))

    return render_template('product_token.html')

@fruutty_token_bp.route('/sent-tokens', methods=['GET', 'POST'])
@login_required
def sent_tokens():
    rep = 'rep'
    if current_user.role == rep:
        flash('login to access this page')
        return render_template('index.html')
    """
        sent_tokens = []
        received_tokens = []
        notifications = []
        """
    user_sent_tokens = db.session.execute(db.select(Sent_tokens).filter_by(user_id=current_user.user_id)).scalars()
    # user_sent_tokens = db.session.execute(db.select(Sent_tokens).order_by(Sent_tokens.receiver)).scalar()
    for tokens in user_sent_tokens:
        sent_token_notification_list = []
        user_sent_tokens_list = []
        user_sent_tokens_list.append(tokens.id)
        user_sent_tokens_list.append(tokens.user_id)
        user_sent_tokens_list.append(tokens.token_reference)
        user_sent_tokens_list.append(tokens.token_amount)
        user_sent_tokens_list.append(tokens.token_value)
        user_sent_tokens_list.append(tokens.receiver)
        user_sent_tokens_list.append(tokens.date)
        sent_token_notification_list.append(user_sent_tokens_list)
        print('notifications', sent_token_notification_list)
        return sent_token_notification_list

    try:
        print('The List : ', user_sent_tokens_list[0])
        return render_template('sent_tokens.html', sent_token_notification_list=sent_token_notification_list)
    except UnboundLocalError:
        return render_template('sent_tokens.html', sent_token_notification_list=None)


@fruutty_token_bp.route('/received-tokens', methods=['GET', 'POST'])
@login_required
def received_tokens():
    rep = 'rep'
    if current_user.role == rep:
        flash('login to access this page')
        return render_template('index.html')
    """
        sent_tokens = []
        received_tokens = []
        notifications = []
        """
    user_received_tokens = db.session.execute(db.select(Received_tokens).filter_by(user_id=current_user.user_id)).scalars()
    # user_sent_tokens = db.session.execute(db.select(Sent_tokens).order_by(Sent_tokens.receiver)).scalar()
    for tokens in user_received_tokens:
        received_token_notification_list = []
        user_received_tokens_list = []
        user_received_tokens_list.append(tokens.id)
        user_received_tokens_list.append(tokens.user_id)
        user_received_tokens_list.append(tokens.token_reference)
        user_received_tokens_list.append(tokens.token_amount)
        user_received_tokens_list.append(tokens.token_value)
        user_received_tokens_list.append(tokens.sender)
        user_received_tokens_list.append(tokens.date)
        received_token_notification_list.append(user_received_tokens_list)
        print('notifications', received_token_notification_list)
    try:
        return render_template('received_tokens.html',
                               user_received_tokens=user_received_tokens,
                               user_received_tokens_list=user_received_tokens_list,
                               received_token_notification_list=received_token_notification_list,

                              )
    except UnboundLocalError:
        return render_template('received_tokens.html',
                               user_received_tokens=None,
                               user_received_tokens_list=None,
                               received_token_notification_list=None,)

@fruutty_token_bp.route('/my-tokens', methods=['GET', 'POST'])

def my_tokens():

    user_tokens = current_user.fruutty_token

    return render_template('my_tokens.html', user_tokens=user_tokens)


@fruutty_token_bp.route('/my-transactions', methods=['GET', 'POST'])
@login_required
def my_transactions():
    rep = 'rep'
    if current_user.role == rep:
        flash('login to access this page')
        return render_template('index.html')
    user_transactions = db.session.execute(
        db.select(Fruutty_transactions).filter_by(user_id=current_user.user_id)).scalars()
    # user_sent_tokens = db.session.execute(db.select(Sent_tokens).order_by(Sent_tokens.receiver)).scalar()
    for transactions in user_transactions:
        user_transaction_list = []
        user_made_transaction_list = []
        user_made_transaction_list.append(transactions.id)
        user_made_transaction_list.append(transactions.user_id)
        user_made_transaction_list.append(transactions.token_id)
        user_made_transaction_list.append(transactions.token_type)
        user_made_transaction_list.append(transactions.product_name )
        user_made_transaction_list.append(transactions.store_name )
        user_made_transaction_list.append(transactions.token_amount)
        user_made_transaction_list.append(transactions.from_owner)
        user_made_transaction_list.append(transactions.location)

        user_made_transaction_list.append(transactions.date)
        user_transaction_list.append(user_made_transaction_list)
        print('notifications', user_transaction_list)
    try:

    # print(len(user_transaction_list))

        for transact in user_transaction_list:
            counter = 0
            print(counter)
            print('Transactions', transact )
            counter += 1
        employee_login = Employee_login(
            employee_id=random_chars(8),
            employee_name='Garfield',
            employee_role='agent',
        )
        db.session.add(employee_login)
        db.session.commit()

        try:
            return render_template('my_transactions.html', user_transaction_list=user_transaction_list )
        except UnboundLocalError:
            return render_template('my_transactions.html', user_transaction_list=None)
    except UnboundLocalError:
        return render_template('my_transactions.html', user_transaction_list=None)


@fruutty_token_bp.route('/notifications', methods=['GET', 'POST'])
@login_required
def notifications():
    rep = 'rep'
    if current_user.role == rep:
        flash('login to access this page')
        return render_template('index.html')
    """
    sent_tokens = []
    received_tokens = []
    notifications = []
    """
    user_sent_tokens = db.session.execute(db.select(Sent_tokens).filter_by(user_id=current_user.user_id)).scalars()
    #user_sent_tokens = db.session.execute(db.select(Sent_tokens).order_by(Sent_tokens.receiver)).scalar()
    for tokens in user_sent_tokens:
        notification_list = []
        user_sent_tokens_list = []
        user_sent_tokens_list.append(tokens.id )
        user_sent_tokens_list.append(tokens.user_id)
        user_sent_tokens_list.append(tokens.token_reference)
        user_sent_tokens_list.append(tokens.token_amount)
        user_sent_tokens_list.append(tokens.token_value)
        user_sent_tokens_list.append(tokens.receiver)
        user_sent_tokens_list.append(tokens.date)
        notification_list.append(user_sent_tokens_list)
        print('notifications', notification_list)


    try:
        print(user_sent_tokens)


        return str(notification_list)
    except UnboundLocalError:
        return str(None)



@fruutty_token_bp.route('/token-request/<int:id>/<email>/<role>', methods=['GET', 'POST'])
@login_required
def token_request(id, email, role):
    rep = 'rep'
    if current_user.role == rep:
        flash('login to access this page')
        return render_template('index.html')
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')

    request_token = request.form.get('token_request', False)
    reference = request.form.get('reference', False)

    if request.method == 'POST':
        if 'confirm_email' in session:
            admin_email = session['confirm_email']
            admin_role = Employee_login.query.filter_by(email=admin_email).first()
            ehckme_email = reference
            requester = Users.query.filter_by(email=ehckme_email).first()
            if admin_role.role == 'admin':


                requester.fruutty_token = request_token
                db.session.commit()
                admin_token_requet = Admin_token_request(
                    employee_id=current_user.user_id,
                    employee_name=current_user.role,
                    email=current_user.email,
                    role=current_user.role,
                    token_request=request_token,
                    token_amount=request_token,
                    reference=reference,


                )
                db.session.add(admin_token_requet)
                db.session.commit()
                """
                Query and get Fruutty Token last date update
                """
                request_token_query = db.session.execute(db.select(Fruutty_token).order_by(Fruutty_token.date)).scalars()

                for request_date in request_token_query:
                    request_token_date = []

                    request_token_date.append(request_date.date)
                print(request_token_date[0])
                """
                Use the fetched query to update the token request
                """

                updated_token_query = Fruutty_token.query.filter_by(date=request_token_date[0]).first()


                available_tokens = updated_token_query.available_tokens
                sold_tokens = updated_token_query.sold_tokens
                opening_trade = updated_token_query.opening_trade
                closing_trade = updated_token_query.closing_trade


                sold_token_to_db = float(sold_tokens) + float(request_token)
                base_token = Config.BASE_TOKEN
                initial_base_token = float(base_token)

                available_tokens_to_db = initial_base_token - (sold_token_to_db)

                four_digits = random_chars(4)
                two_digits = random_chars(2)

                admin_fruutty_token_request = Fruutty_token(
                    token_id=Config.TOKEN_ID + four_digits + '_' + two_digits,
                    initial_base_token=Config.BASE_TOKEN,
                    available_tokens=available_tokens_to_db,
                    sold_tokens = sold_token_to_db,
                    opening_trade=opening_trade,
                    closing_trade=closing_trade,

                )
                db.session.add(admin_fruutty_token_request)
                db.session.commit()

                flash('token sent succesfully')
                return redirect(url_for('employees.s_message'))
            else:
                flash('You have to be an admin usser to request tokens')
                return redirect(url_for('employees.s_message'))

    return render_template('token_request.html', id=id , email=email, role=role)


@fruutty_token_bp.route('/fruuty-market', methods=['GET', 'POST'])
@login_required
def fruuty_market():
    """
        ############  Get food imga name from database #############
    """
    food_image = db.session.execute(db.select(Food).order_by(Food.date)).scalars()
    # sleeve = 'Unfinished.jpg'
    for food in food_image:
        food_list = [ ]
        food_picture = str(food.image_name)
        food_link = str(food.link)
        print(food_link)
        print(food_picture)
    try:
        food_image_url = food_picture
        food_link_url = food_link
    except UnboundLocalError:
        food_image_url = None
        food_link_url = None


    """   
        ############  Get Fashion imga name from database #############
    """
    fashion_image = db.session.execute(db.select(Fashion).order_by(Fashion.date)).scalars()
    for fashion in fashion_image:
        fashion_image_name = str(fashion.image_name)
        fashion_image_link = str(fashion.link)
        print(fashion_image_name)
        print(fashion_image_link)
    try:
        fashion_image_url = fashion_image_name
        fashion_link_url = fashion_image_link
    except UnboundLocalError:
        fashion_image_url = None
        fashion_link_url = None
    """   
        ############  Get tech imga name from database #############
    """
    tech_image = db.session.execute(db.select(Tech).order_by(Tech.date)).scalars()
    for tech in tech_image:
        tech_picture = str(tech.image_name)
        tech_link = str(tech.link)
        print(tech_picture)
    try:
        tech_image_url = tech_picture
        tech_link_url = tech_link
    except UnboundLocalError:
        tech_link_url = None
        tech_image_url = None

    """   
        ############  Get song name from database #############
    """

    song = db.session.execute(db.select(Music).order_by(Music.date)).scalars()
    for music in song:

        audio_file_name = str(music.audio_file_name)
        song_name = str(music.song_name)
        artist_name = str(music.artist_name)
        artist_bio = str(music.artist_bio)
        record_company = str(music.record_company)
        image_link = str(music.image_link)
        song_link = str(music.song_link)
        lyrics = str(music.lyrics)

    try:

        audio_file_name_url = audio_file_name
        song_name_url = song_name
        artist_name_url = artist_name
        artist_bio_url = artist_bio
        record_company_url = record_company
        image_link_url = image_link
        song_link_url = song_link
        lyrics_url = lyrics

    except UnboundLocalError:

        audio_file_name_url = None
        song_name_url = None
        artist_name_url = None
        artist_bio_url = None
        record_company_url = None
        image_link_url = None
        song_link_url = None
        lyrics_url = None

    """   
        ############  Get Drive imga name from database #############
    """
    car_image = db.session.execute(db.select(Drive).order_by(Drive.date)).scalars()
    for car in car_image:
        car_image_name = str(car.image_name)
        car_image_link = str(car.link)
        print(car_image_name)
        print(car_image_link)
    try:
        car_image_url = car_image_name
        car_link_url = car_image_link
    except UnboundLocalError:
        car_image_url = None
        car_image_link = None



    return render_template('fruuty_market.html',

                           food_image_url=food_image_url,
                           food_link_url=food_link_url,
                           tech_image_url=tech_image_url,
                           tech_link_url=tech_link_url,
                           car_image_url=car_image_url,
                           car_image_link=car_image_link,
                           fashion_image_url=fashion_image_url,
                           fashion_link_url=fashion_link_url,


                           # Music Section

                           audio_file_name_url=audio_file_name_url,
                           song_name_url=song_name_url,
                           artist_name_url=artist_name_url,
                           artist_bio_url=artist_bio_url,
                           record_company_url=record_company_url,
                           image_link_url=image_link_url,
                           song_link_url=song_link_url,
                           lyrics_url=lyrics_url,

                           )


@fruutty_token_bp.route('/scanner-results', methods=['GET', 'POST'])
@login_required
def scanner_results():
    rep = 'rep'
    if current_user.role == rep:
        flash('login to access this page')
        return render_template('index.html')
    return render_template('scanner_results.html')

@fruutty_token_bp.route('/paid-sales', methods=['GET', 'POST'])
def paid_sales():
    data = [{'discount': 'none'},
            {'discount': '5%'}, {'discount': '10%'},
            {'discount': '15%'}, {'discount': '20%'},
            {'discount': '25%'}, {'discount': '30%'},
            {'discount': '35%'}, {'discount': '40%'},
            {'discount': '45%'}, {'discount': '50%'}]

    return render_template('paid_sales.html', data=data)


@fruutty_token_bp.route('/lyric-modal', methods=['GET', 'POST'])
def lyric_modal():
    return render_template('lyric_modal.html')

@fruutty_token_bp.route('/start-app', methods=['GET', 'POST'])
def start_app():
    currency_pair = Currency_Pairs()
    sa_rand = 1
    usd_zar = currency_pair.usd_zar()
    gbp_zar = currency_pair.gbp_zar()
    kwd_zar = currency_pair.kwd_zar()
    cny_zar = currency_pair.cny_zar()

    kwd_to_zar = 1 / kwd_zar
    gbp_to_zar = 1 / gbp_zar
    cny_to_zar = 1 / cny_zar
    print('KWD TO ZAR ## ', kwd_to_zar)
    print('KWD TO ZAR ## ', gbp_to_zar)

    total_number_of_currencies = 5
    total = sa_rand + usd_zar + gbp_to_zar + kwd_to_zar + cny_to_zar
    average = total / total_number_of_currencies

    four_digits = random_chars(4)
    two_digits = random_chars(2)

    ftvs_model = Ftvs(
        south_african_rand=sa_rand,
        united_states_dollar=usd_zar,
        british_pound=gbp_to_zar,
        kuwaiti_dinar=kwd_to_zar,
        chinese_yuan=cny_to_zar,
        average=average,
        total=total,
    )

    fruutty_token = Fruutty_token(
        token_id=Config.TOKEN_ID + four_digits + '_' + two_digits,
        initial_base_token=Config.BASE_TOKEN,
        opening_trade=average,

    )
    role = 'admin'
    admin_role_in_db = Users.query.filter_by(role=role).first()
    admin_role = admin_role_in_db.role

    admin_login = Employee_login(
        employee_id=admin_role_in_db.user_id,
        employee_name=admin_role_in_db.username,
        email=admin_role_in_db.email,
        password=admin_role_in_db.password,
        role=admin_role_in_db.role,
        lastLogin_at=func.now(),

    )

    db.session.add(fruutty_token)
    db.session.add(ftvs_model)
    db.session.add(admin_login)
    db.session.commit()
    # render_template('start_app.html')

    return Config.BASE_TOKEN


@fruutty_token_bp.route('/updater', methods=['GET', 'POST'])
@login_required
def updater():

    return str(0)

@fruutty_token_bp.route('/backup', methods=['GET', 'POST'])
def backup():

    # render_template('backup.html')

    return str(0)



