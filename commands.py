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
 
    katie = User(
        user_name = "katie",
        user_email = "katieW@gmail.com",
        user_mast_password = bcrypt.generate_password_hash("Kath43").decode('utf-8'), 
        user_admin = False
    )
    db.session.add(katie)
    db.session.commit()
    
    
    entry1 = Entry(
        ent_url = "guns&ammo.com",
        ent_pswd = "kathode1",
        ent_username = "kathTheGreat",
        ent_email = "katieW@gmail.com",
        user_id = 3
    )
    db.session.add(entry1)

    entry2 = Entry(
        ent_url = "poolRus.com",
        ent_pswd = "poolmaniac",
        ent_username = "Gazza",
        ent_email = "garry54@hotmail.com",
        user_id = 2
    )
    db.session.add(entry2)

    db.session.commit()
    print("Table seeded")