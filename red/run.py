from flask import Flask, flash, jsonify, render_template, redirect, url_for, request, abort, \

    session, make_response, g

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

from datetime import timedelta

from os import listdir # directorios 

from werkzeug.utils import secure_filename # subir archivos a los servidor 

# from flask_wtf.csrf import CsrfProtect



login_manager = LoginManager()

login_manager.login_view   = "usr.login"

login_manager.refresh_view = 'relogin'

login_manager.needs_refresh_message = (u"Session timedout, please re-login")

login_manager.needs_refresh_message_category = "info"



db   = SQLAlchemy()

   

def create_app():

    from red.views import pub

    

    app = Flask(__name__, static_url_path='/static')  

    app.config.from_object('red.config')

    db.init_app(app)

    

    login_manager.init_app(app)

 

    app.register_blueprint(pub)

 

    @app.before_request

    def before_request():

        session.permanent = True

        

    @login_manager.user_loader

    def load_user(user_id):

        from .models import Usuarios

        return Usuarios.query.get(int(user_id))

            

    return app