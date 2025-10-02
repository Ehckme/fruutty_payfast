from flask import Flask
from flask import flash
from flask import Blueprint
from flask import request, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required

fruutty_docs_bp = Blueprint('fruutty_docs', __name__,
                             template_folder='templates',
                             )


@fruutty_docs_bp.route('/fruutty-docs')
def fruutty_docs():
    return render_template('fruutty-docs.html')

