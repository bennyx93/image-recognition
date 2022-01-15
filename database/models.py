from .db import db


class Tag(db.Document):
    name = db.StringField(required=True, unique=True)


class Image(db.Document):
    name = db.StringField(required=True)
    file = db.ImageField(required=True)
    tags = db.ListField(db.ReferenceField(Tag), required=False)
