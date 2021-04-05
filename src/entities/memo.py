from mongoengine import Document, StringField, ObjectIdField, DateTimeField


class Memo(Document):
    author_id = ObjectIdField(required=True)
    title = StringField(required=True, max_length=100)
    content = StringField()
    date = DateTimeField(required=True)
