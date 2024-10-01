from flask import Blueprint
from flask import flash
from flask import request, render_template, url_for, redirect

# import OTP
from authentication.database.extensions import OTP, session, db
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

# import flask login
from flask_login import login_required, current_user, logout_user


logout_bp = Blueprint('logout', __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/logout/static',
                      )


@logout_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    email = current_user.email
    user_logout_time = Users.query.filter_by(email=email).first()

    user_logout_time.lastLout_at = func.now()
    db.session.commit()

    logout_user()
    return render_template('index.html')