import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, request, abort
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from marshmallow.validate import Length
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy 
from datetime import date, timedelta

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.app_config")
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    from commands import db_commands
    app.register_blueprint(db_commands)
    
    # import controllers and activate their blueprints
    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)
    
    return app

    

     
# ROUTES ------------------------------
    
# @app.route("/")
# def index():
#     return "Welcome to my Password Manager"


