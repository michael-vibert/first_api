from main import db 

class Entry (db.Model):
    __tablename__ = "entries"
    
    ent_id = db.Column(db.Integer, primary_key=True)
    ent_url = db.Column(db.String, nullable=False)
    ent_pswd = db.Column(db.String, nullable=False)
    ent_username = db.Column(db.String, nullable=True)
    ent_email = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)