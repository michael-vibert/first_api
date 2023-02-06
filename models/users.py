from main import db 

class User(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(), nullable=False, unique=True)
    user_email = db.Column(db.String(), nullable=False, unique=True)
    user_mast_password = db.Column(db.String(), nullable=False, unique=True)
    user_admin = db.Column(db.Boolean(), default=False)
    