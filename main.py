from flask import Flask, jsonify, request, abort
app = Flask(__name__)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

app.config["JWT_SECRET_KEY"] = "Super secret never guess key"
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
jwt = JWTManager(app)

from marshmallow.validate import Length
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

from flask_sqlalchemy import SQLAlchemy 
# set the database URI via SQLAlchemy,     dbms       
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://mike_v:12345@localhost:5432/wombat_logon_db"
# to avoid the deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#create the database object
db = SQLAlchemy(app)

from datetime import date, timedelta

#  COMMANDS AREA---------------------

@app.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")
    
@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 
    
@app.cli.command("seed")
def seed_db():
    admin_user = User(
        # user_id = 001,
        user_name = "admin",
        user_email = "mike1234@hotmail.com",
        user_mast_password = bcrypt.generate_password_hash("AcroMan32").decode('utf-8'),
        user_admin = 1
    )
    
    db.session.add(admin_user)
    garry = User(
        # user_id = 002,
        user_name = "garry",
        user_email = "garry54@hotmail.com",
        user_mast_password = bcrypt.generate_password_hash("passwords").decode('utf-8'), 
        user_admin = False
    )
    db.session.add(garry)
    db.session.commit()
    print("Table seeded")

# MODELS AREA ------------------------

class User(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(), nullable=False, unique=True)
    user_email = db.Column(db.String(), nullable=False, unique=True)
    user_mast_password = db.Column(db.String(), nullable=False, unique=True)
    user_admin = db.Column(db.Boolean(), default=False)
    
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        user_master_password = ma.String(validate=Length(min=8))
        
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Entry (db.Model):
    __tablename__ = "entries"
    
    ent_id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    ent_url = db.Column(db.String, nullable=False)
    ent_pswd = db.Column(db.String, nullable=False)
    ent_username = db.Column(db.String, nullable=True)
    ent_email = db.Column(db.String, nullable=True)
    
class EntrySchema(ma.Schema):
    class Meta:
        fields = ("ent_id", "ent_url", "ent_pswd", "ent_username", "ent_email")

entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)   
     
# ROUTES ------------------------------
    
@app.route("/")
def index():
    return "Welcome to my Password Manager"


@app.route("/entry/add", methods=["POST"])
@jwt_required()
def add_entry():
    entry_fields = entry_schema.load(request.json)
    
    new_entry = Entry()
    new_entry.ent_id = entry_fields["ent_id"]
    new_entry.ent_url = entry_fields["ent_url"]
    new_entry.ent_pswd = entry_fields["ent_pswd"]
    new_entry.ent_username = entry_fields["ent_username"]
    new_entry.ent_email = entry_fields["ent_email"]
    
    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify(entry_schema.dump(new_entry))


@app.route("/auth/register", methods=["POST"])
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

@app.route("/auth/login", methods=["POST"])
def auth_login():
    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(user_name=user_fields["user_name"]).first()
    if not user or not bcrypt.check_password_hash(user.user_mast_password, user_fields["user_mast_password"]):
        return abort(401, description="Incorrect username and/or password")
    
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.user_name), expires_delta=expiry)
    return jsonify({"user": user.user_name,  "token": access_token})