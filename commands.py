from main import db
from flask import Blueprint
from main import bcrypt
from models.users import User
from models.entries import Entry
from datetime import date

db_commands = Blueprint("db", __name__)
 
 
@db_commands .cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

    
@db_commands .cli.command("drop_tables")
def drop_tables():
    db.drop_all()
    print("All tables in db dropped")

    
@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 

    
@db_commands .cli.command("seed")
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