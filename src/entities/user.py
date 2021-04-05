from mongoengine import Document, StringField, ListField, ObjectIdField


class User(Document):
    firstname = StringField(required=True, max_length=25)
    lastname = StringField(required=True, max_length=25)
    username = StringField(required=True, max_length=40, unique=True)
    password = StringField(required=True)
    memos = ListField(ObjectIdField(), default=list)
