import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from functools import wraps

from flask import Flask
from flask import flash
from flask import Blueprint
from flask import request, render_template, redirect, url_for, g
from flask_login import UserMixin, LoginManager, current_user, login_required

from authentication.database.model import (Applications, Employees,
                                           Employee_login, Employee_address,
                                           Users, Ftvs, Fruutty_token,
                                           Admin_token_request
                                           )
from authentication.database.extensions import db, session, OTP
from uconra.register import Register, random_chars, SMTP_Mail
from uconra.email_message import MailMessage
from uconra.j_wt import JWT

from config import Config

employees_bp = Blueprint('employees', __name__,
                         template_folder='templates',
                         static_folder='static',
                         static_url_path='/static/employess',
                         )

"""
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
    
"""

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

@employees_bp.route('/admin/<int:id>/<email>/<role>', methods=['GET', 'POST'])
@login_required
def admin(id, email, role):
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')
    users = Users.query
    print(users)
    number_of_users = 0
    for user in users:
        number_of_users += 1

    print('counter : ', number_of_users)

    trade_token_query = db.session.execute(db.select(Ftvs).order_by(Ftvs.date)).scalars()
    for value in trade_token_query:
        trade_token_value = []
        trade_token_value.append(value.average)

    available_tokens_query = db.session.execute(db.select(Fruutty_token).order_by(Fruutty_token.date)).scalars()
    for av_tokens in available_tokens_query:
        available_tokens = []
        available_tokens.append(av_tokens.available_tokens)

    sold_token_query = db.session.execute(db.select(Fruutty_token).order_by(Fruutty_token.date)).scalars()
    for s_tokens in sold_token_query:
        sold_tokens = []
        sold_tokens.append(s_tokens.sold_tokens)


    # print('Trade Token Value : ', trade_token_value[0])


    return render_template('admin.html',
                           session_role=get_admin.role,
                           id=get_admin.id,
                           email=get_admin.email,
                           role=get_admin.role,
                           users=users,
                           number_of_users=number_of_users,
                           trading_token_value=trade_token_value[0],
                           available_tokens=available_tokens[0],
                           sold_tokens=sold_tokens[0],


                           )

@employees_bp.route('/admin-id/<int:id>/<email>/<role>', methods=['GET', 'POST'])
@login_required
def admin_id(id, email, role):
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')

    get_admin_id = request.form.get('admin_id', False)
    employee_id = Employee_login.query.filter_by(employee_id=get_admin_id).first()
    print(employee_id)

    if request.method == 'POST':
        try:
            if employee_id.role == 'admin':

                return redirect(url_for('fruutty_token.token_request', id=current_user.id, email=current_user.email, role=current_user.role))
        except AttributeError:

            message = 'Invalid id'
            flash(f'{message}')
            return redirect(url_for('employees.s_message', message=message))

    return render_template('admin_id.html', id=current_user.id, email=current_user.email, role=current_user.role)


@employees_bp.route('/employees/<int:id>/<email>/<role>', methods=['GET', 'POST'])
@login_required
def employees(id, email, role):
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')

    return render_template('employees.html',
                           id=current_user.id,
                           email=current_user.email,
                           role=current_user.role)

@employees_bp.route('/employee-login', methods=['GET', 'POST'])
def employee_login():

    return render_template('employee_login.html')

@employees_bp.route('/employee-login', methods=['GET', 'POST'])
def add_employee():

    return render_template('employee_login.html')

@employees_bp.route('/applications', methods=['GET', 'POST'])
@login_required
def applications():
    name = request.form.get('name', False)
    surname = request.form.get('surname', False)
    email = request.form.get('email', False)
    cell = request.form.get('cell', False)

    street_name = request.form.get('street_name', False)
    house_number = request.form.get('house_number', False)
    area_name = request.form.get('area_name', False)
    postal_code = request.form.get('postal_code', False)

    city = request.form.get('city', False)
    province = request.form.get('province', False)
    country = request.form.get('country', False)

    if request.method == 'POST':

        application = Applications(
            name=name, surname=surname,
            email=email, cell=cell,
            street_name=street_name, house_number=house_number,
            area_name=area_name, postal_code=postal_code,
            city=city, province=province,
            country=country,
            application_date=func.now(),
        )
        db.session.add(application)
        db.session.commit()
        message = 'Application Sent Successfully'
        flash(message=message)
        return render_template('s_message.html')

    return render_template('applications.html')

@employees_bp.route('/employee-application', methods=['GET', 'POST'])
def employee_application():
    return render_template('employee_application.html')

@employees_bp.route('/applicants/<int:id>/<email>/<role>', methods=['GET', 'POST'])
# @login_required
def applicants(id, email, role):
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')

    if request.method == 'POST':
        applicant = db.session.execute(db.select(Applications).order_by(Applications.application_date)).scalars()
        message = 'Applicant approved'

        print(applicant)
        for item in applicant:
            applicant_list = []
            applicant_list.append(item.email)
            print(item.email)
        try:
            item.approoved = True;

            employee_user = Users(
                user_id='fruutty' + '-' + random_chars(8) + '-' + 'employee',
                username=item.name,
                email=item.email,
                confirmed=True,
                country=item.country,
                password='null',
                role='rep'

            )
            db.session.add(employee_user)
            db.session.commit()

            employee_id_in_db = Users.query.filter_by(email=item.email).first()
            employee_id_from_db = employee_id_in_db.user_id


            employee = Employees(
                employee_id=employee_id_from_db,
                name=item.name,
                surname=item.surname,
                email=item.email,
                cell=item.cell,
                department='sales',
                role='rep',
            )
            db.session.add(employee)
            db.session.commit()

            id = Employees.query.filter_by(email=item.email).first()
            employee_id = id.employee_id

            print('employee id ', employee_id)

            employee_address = Employee_address(
                employee_id=employee_id,
                name=item.name,
                street_name=item.street_name,
                house_number=item.house_number,
                area_name=item.area_name,
                postal_code=item.postal_code,
                city=item.city,
                province=item.province,
                country=item.country,
            )
            db.session.add(employee_address)
            db.session.commit()

            employee_login = Employee_login(
                employee_id=employee_id,
                employee_name=id.name,
                email=id.email,
                password='null',
                role=id.role,
            )
            db.session.add(employee_login)
            db.session.commit()
            """ -------- Create email message ---------- """
            # token
            # assign a token variable
            token = JWT()
            # Generate a user token
            user_token = token.generate_jwt_token(applicant_list[0], key=Config.FLASK_SECRET_KEY)
            print('applicant_list ', applicant_list[0])
            print(user_token)
            approve_message = MailMessage()

            employee_id_from_login_db = Employee_login.query.filter_by(email=applicant_list[0]).first()
            employee_id_to_send = employee_id_from_login_db.employee_id
            sendMail = SMTP_Mail(
                appKey=Config.APP_PASSWORD, userMail=applicant_list[0],
                senderMail=Config.UCONRA_EMAIL, serverEhlo=Config.SERVER_EHLO,
                smtpServer=Config.SMTP_EMAIL_SERVER,
                subject='APPLICATION APPROVED', userName=applicant_list[0].split('@')[1],
                message=approve_message.approve_message(token=applicant_list[0], content=employee_id_to_send),
            )
            """ -------- Send email ---------- """
            sendMail.sendMail()

            flash(f'{message} {item.email} {item.name} {item.cell}')
            return redirect(url_for('employees.s_message', item=item.email))
        except UnboundLocalError:
            message = 'No applicant to approve'
            flash(message=message)
            return redirect(url_for('employees.s_message'))

    applicant = db.session.execute(db.select(Applications).order_by(Applications.application_date)).scalars()
    for item in applicant:
        applicant_list = []
        applicant_list.append(item.email)
        print(item.email)
    try:

        flash(f'{item.email} {item.name} {item.cell}')
        return render_template('applicants.html',
                               id=current_user.id, email=current_user.email,
                               role=current_user.role, item=item.email
                               )
    except UnboundLocalError:
        return render_template('applicants.html', id=current_user.id,
                               email=current_user.email,
                               role=current_user.role,
                               item=None
                               )

@employees_bp.route('/employment-id/<email>', methods=['GET', 'POST'])
def employment_id(email):
    email_in_db = Users.query.filter_by(email=email).first()
    emp_email = email_in_db.email
    if emp_email != email:
        return render_template('index.html')



    request_id = request.form.get('employee_id', False)
    employee_db_id = Employees.query.filter_by(employee_id=request_id).first()
    employee_db_logn_id = Employee_login.query.filter_by(employee_id=request_id).first()

    if request.method == 'POST':
        session['emp_id'] = request_id
        try:

            if (employee_db_id.employee_id and employee_db_logn_id.employee_id == request_id
                    and employee_db_logn_id.password == 'null'):

                return redirect(url_for('employees.create_emp_password'))

            elif (employee_db_id.employee_id and employee_db_logn_id.employee_id == request_id
                  and employee_db_logn_id.password != 'null'):

                return redirect(url_for('login.login'))

            else:
                message = 'Invalid id'
                flash(f'{message}')

                return redirect(url_for('employees.s_message', message=message))

        except AttributeError:

            message = 'Invalid id'
            flash(f'{message}')
            return redirect(url_for('employees.s_message', message=message))


    return render_template('employment_id.html', email=email)

@employees_bp.route('/create-emp-password', methods=['GET', 'POST'])
def create_emp_password():

    password = request.form.get('password', False)
    re_type_password = request.form.get('re_type_password', False)


    if request.method == 'POST':
        if 'emp_id' in session:
            emp_id = session['emp_id']
            get_emp_id = Employee_login.query.filter_by(employee_id=emp_id).first()
            if password != re_type_password:
                message = 'password do not match'
                flash(f'{message}')
                return redirect(url_for('employees.s_message', message=message))
            else:
                register = Register()
                get_emp_id.password = register.userPassword(re_type_password)
                send_password_to_users = Users.query.filter_by(email=get_emp_id.email).first()
                send_password_to_users.password = get_emp_id.password
                print('get-emp_id', get_emp_id.password)
                db.session.commit()

                send_password_to_users = Users.query.filter_by(email=get_emp_id.email).first()
                send_password_to_users.password = get_emp_id.password
                print('send_password_to_users', send_password_to_users.password)
                db.session.commit()
                return redirect(url_for('fruutty_token.index'))

    return render_template('create_emp_password.html')

@employees_bp.route('/sales/<int:id>/<email>/<role>', methods=['GET', 'POST'])
@login_required
def sales(id, email, role):
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')

    return render_template('sales.html',
                           id=current_user.id,
                           email=current_user.email,
                           role=current_user.role)

@employees_bp.route('/confirm-emp-id/<int:id>/<email>/<role>', methods=['GET', 'POST'])

def confirm_emp_id(id, email, role):
    if 'confirm_email' in session:
        admin_session = session['confirm_email']
        get_admin = Users.query.filter_by(email=admin_session).first()

        if get_admin.id != id and get_admin.email != email and get_admin.role != role:
            return render_template('index.html')


    get_employee_id = request.form.get('confirm_emp_id', False)
    employee_id = Users.query.filter_by(user_id=get_employee_id).first()


    if request.method == 'POST':
        try:
            if employee_id.role == 'rep':

                return redirect(url_for('employees.sales',
                                        id=current_user.id,
                                        email=current_user.email,
                                        role=current_user.role

                                        ))
        except AttributeError:

            message = 'Invalid id'
            flash(f'{message}')
            return redirect(url_for('employees.s_message', message=message))


    return render_template('confirm_emp_id.html',
                           id=current_user.id,
                           email=current_user.email,
                           role=current_user.role)



@employees_bp.route('/s-message', methods=['GET', 'POST'])
def s_message():

    return render_template('s_message.html')