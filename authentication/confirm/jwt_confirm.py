import jwt
import datetime
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

jwt_confirm_bp = Blueprint('jwt_confirm', __name__,
                           template_folder='templates',
                           static_folder='static',
                           static_url_path='/login/static'
                           )

@jwt_confirm_bp.route('/jwt-confirm/<token>', methods=['GET', 'POST'])

def jwt_confirm(token):
    email = JWT()
    try:
        try:
            user_token = email.decode_jwt_token(token)
            user_email_in_db = Users.query.filter_by(email=user_token['email']).first()
            if user_email_in_db:
                user_email_in_db.confirmed = True
                user_email_in_db.confirmed_at = func.now()
                db.session.commit()
                flash('Your email is confirmed')
                print('User is confirmed')
                return render_template('jwt_confirm.html')
        except jwt.ExpiredSignatureError:
            return redirect(url_for('resend_token.resend_token'))
    except jwt.DecodeError:
        flash('Invalid token')
        return redirect(url_for('invalid_token.invalid_token'))

    return render_template('jwt_confirm.html', token=token, )