"""############ import flask and all necessary modules #############"""
from flask import Flask
from flask import flash
from flask import Blueprint
from flask import request, render_template, redirect, url_for

dashboard_bp = Blueprint('dashboard', __name__,
                         template_folder='templates',
                         static_folder='static',
                         static_url_path=''
                         )

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')