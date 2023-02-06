from main import db 

class Entry (db.Model):
    __tablename__ = "entries"
    
    ent_id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    ent_url = db.Column(db.String, nullable=False)
    ent_pswd = db.Column(db.String, nullable=False)
    ent_username = db.Column(db.String, nullable=True)
    ent_email = db.Column(db.String, nullable=True)