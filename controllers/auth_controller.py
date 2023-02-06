from flask import Blueprint, jsonify, request, abort
from main import db
from models.users import User
from schemas.users_schema import user_schema, users_schema
from datetime import timedelta
from main import bcrypt
from flask_jwt_extended import create_access_token


auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.post("/register")
def auth_register():
    
    user_fields = user_schema.load(request.json)
    test = User.query.filter_by(user_email=user_fields["user_email"]).first()
    
    if test:        
        return abort(400, description="Email already registered")
    
    user = User()
    user.user_name = user_fields["user_name"]
    user.user_email = user_fields["user_email"]
    user.user_mast_password = bcrypt.generate_password_hash(user_fields["user_mast_password"]).decode("utf-8")
    
    db.session.add(user)
    db.session.commit()
    
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.user_name), expires_delta=expiry)
    return jsonify({"user": user.user_name, "token": access_token})

@app.post("/login")
def auth_login():
    # load up the posted data 
    user_fields = user_schema.load(request.json)
    # check the database for the user\
    user = User.query.filter_by(user_name=user_fields["user_name"]).first()
    # check that user exisits and check password matches
    if not user or not bcrypt.check_password_hash(user.user_mast_password, user_fields["user_mast_password"]):
        return abort(401, description="Incorrect username and/or password")
    # set expiry for the jwt token
    expiry = timedelta(days=1)
    # create the token then send it back to the user
    access_token = create_access_token(identity=str(user.user_name), expires_delta=expiry)
    return jsonify({"user": user.user_name,  "token": access_token})