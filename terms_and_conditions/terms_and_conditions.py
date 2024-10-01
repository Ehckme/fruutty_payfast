from flask import Flask
from flask import flash
from flask import Blueprint
from flask import request, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required


terms_and_conditions_bp = Blueprint('terms_and_conditions', __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='/static/fruutty_token',
                             )

@terms_and_conditions_bp.route('/about', methods=['GET', 'POST'])
def about():

    return render_template('about.html')

@terms_and_conditions_bp.route('/terms-and-conditions', methods=['GET', 'POST'])
def terms_and_conditions():

    return render_template('terterms_and_conditions.html')

@terms_and_conditions_bp.route('/privacy-policy', methods=['GET', 'POST'])
def privacy_policy():

    return render_template('privacy_policy.html')

@terms_and_conditions_bp.route('/cookie-policy', methods=['GET', 'POST'])
def cookie_policy():

    return render_template('cookie_policy.html')