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


account_active_bp = Blueprint('account_active', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='/login/static',
                            )


@account_active_bp.route('/account-active', methods=['GET', 'POST'])
def account_active():
    if request.method == 'POST':
        return redirect(url_for('login.login'))
    return render_template('account_active.html')