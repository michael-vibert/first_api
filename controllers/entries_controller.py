
from flask import Blueprint, jsonify, request, abort
from main import db
from models.entries import Entry
from models.users import User
from schemas.entry_schema import entry_schema, entries_schema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

entry = Blueprint("entry", __name__, url_prefix="/entry")

@entry.post("/add")
@jwt_required()
def add_entry():
    entry_fields = entry_schema.load(request.json)
    
    new_entry = Entry()
    new_entry.ent_url = entry_fields["ent_url"]
    new_entry.ent_pswd = entry_fields["ent_pswd"]
    new_entry.ent_username = entry_fields["ent_username"]
    new_entry.ent_email = entry_fields["ent_email"]
    
    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify(entry_schema.dump(new_entry))

# deletes the indicated entry via the ent_id/ must pass attach valid jwt
@entry.delete("/<int:id>/")
@jwt_required()
def delete_entry(id):
    # grab the users id using the jwt helper methods 
    user_name = get_jwt_identity()
    print(user_name)
    
    # find the user in db
    user1 = User.query.filter_by(user_name = user_name)
    if not user1:
        return abort(401, description="Invalid user")
    # check to see if entry in the db
    entry = Entry.query.filter_by(ent_id=id).first()
    if not entry:
        return abort(400, description="Entry doesn't exist") 
    
    
    
    db.session.delete(entry)
    db.session.commit()
    return jsonify(entry_schema.dump(entry))

# get all the entires
@entry.get("/entries")
def get_entries():
    entries_list = Entry.query.all()
    print(entries_list) 
    data = entries_schema.dump(entries_list)
    print(data)
    return jsonify(data)


@entry.get("/<int:ent_id>")
def get_entry(ent_id):
    entry = Entry.query.get(ent_id)
    data = entry_schema.dump(entry)
    return jsonify(data)