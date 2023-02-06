from main import ma


class EntrySchema(ma.Schema):
    class Meta:
        fields = ("ent_id", "ent_url", "ent_pswd", "ent_username", "ent_email")
# must define an instance to use
entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)