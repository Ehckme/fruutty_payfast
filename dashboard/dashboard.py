"""############ import flask and all necessary modules #############"""
from flask import Flask
from flask import flash
from flask import Blueprint
from flask_login import login_required, current_user
from authentication.database.extensions import db
from config import Config
import datetime
import uuid
from flask import request, render_template, redirect, url_for
from authentication.database.model import (TokenPurchase, Users, Fruutty_transactions,
                                           Fruutty_token, Ftvs,
                                           Sent_tokens, Received_tokens,
                                           Notifications, Food,
                                           Fashion, Drive,
                                           Tech, Music, Employee_login, Admin_token_request,
                                           )

dashboard_bp = Blueprint('dashboard', __name__,
                         template_folder='templates',
                         static_folder='static',
                         static_url_path=''
                         )


@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Get current user token balance
    user_tokens = current_user.fruutty_token or 0

    # Fetch latest FTVS trade value
    ftvs = Ftvs.query.order_by(Ftvs.date.desc()).first()
    ftvs_value = ftvs.average if ftvs else 0.0  # use 'average' as trade value

    # Fetch the most recent transaction
    recent_transaction = (
        TokenPurchase.query.filter_by(user_id=current_user.id)
        .order_by(TokenPurchase.created_at.desc())
        .first()
    )

    # Fetch user notifications
    notifications = (
        Notifications.query.filter_by(user_id=current_user.id)
        .order_by(Notifications.date.desc())
        .all()
    )

    return render_template(
        'dashboard.html',
        user_tokens=user_tokens,
        ftvs_value=ftvs_value,
        recent_transaction=recent_transaction,
        notifications=notifications
    )

