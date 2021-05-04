from mongoengine import Document, StringField, ReferenceField, DateTimeField


class Memo(Document):
    """Class for memo objects. Inherits from mongonengines document class
    by giving all functions from that. Class defines types for database.

    author is required reference to User; when object is got from database, is replaced
    with user object. Holds information of memo's author.

    title is required string, limited length 50 characters. Holds title for memo.

    content is string, holds memo's content - what user has written.

    date is required datetime, holds info about when memo was created.
    """
    author = ReferenceField('User', required=True)
    title = StringField(required=True, max_length=50)
    content = StringField()
    date = DateTimeField(required=True)
