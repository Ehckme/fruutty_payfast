from flask import Flask
from flask import flash
from flask import Blueprint
from flask import request, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, current_user, login_required

from authentication.database.model import Employees, Employee_login, Music, Users
from authentication.database.extensions import db, OTP


import json

import io
import base64
from PIL import Image

fruuty_player_bp = Blueprint('fruutty_player', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='/static/fruutty_player',
                            )

@fruuty_player_bp.route('/fruuty-player', methods=['GET', 'POST'])
@login_required
def fruuty_player():
    """
        ############  Get tech imga name from database #############
    """
    song = db.session.execute(db.select(Music).order_by(Music.date)).scalars()
    for music in song:
        audio_file_name = str(music.audio_file_name)
        print(audio_file_name)
    audio_file_name_url = audio_file_name

    return render_template('fruutty_player.html', audio_file_name_url=audio_file_name_url )