
from flask import Blueprint, jsonify, request, abort
from main import db
from models.entries import Entry
from models.users import User
from schemas.entry_schema import entry_schema
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


@entry.get("/entries")
def get_entries():
    entries_list = Entry.query.all()
    print(entries_list) 
    
    return jsonify(entry_schema.dump(entries_list))


@entry.get("/entries/<int:ent_id>")
def get_entry(ent_id):
    entry = Entry.query.get(ent_id)
    data = entry_schema.dump(entry)
    return jsonify(data)