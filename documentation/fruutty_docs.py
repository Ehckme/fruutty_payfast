from flask import Flask
from flask import flash
from flask import Blueprint
from flask import request, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required

documentation_bp = Blueprint('documentation', __name__,
                             template_folder='templates',
                             )


@documentation_bp.route('/fruutty-docs')
def fruutty_docs():
    return render_template('fruutty_docs.html')
