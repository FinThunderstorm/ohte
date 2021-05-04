from mongoengine import Document, StringField, ListField, ReferenceField


class User(Document):
    """Class for user objects. Inherits from mongonengines document class
    by giving all functions from that. Class defines types for database.

    firstname is required string, limited length 25 characters.
    Holds user's firstname.

    lastname is required string, limited length 25 characters.
    Holds user's lastname.

    username is required string, limited length 40 characters.
    Holds user's username. Needs to be unique, checked in database
    when creating new user.

    password is required string, should be given as encrypted.

    memos is list, that references to memos created by user. Defaults
    to empty list.
    """
    firstname = StringField(required=True, max_length=25)
    lastname = StringField(required=True, max_length=25)
    username = StringField(required=True, max_length=40, unique=True)
    password = StringField(required=True)
    memos = ListField(ReferenceField('Memo'), default=list)
