from mongoengine import Document, StringField, ReferenceField, DateTimeField


class Memo(Document):
    author = ReferenceField('User', required=True)
    title = StringField(required=True, max_length=100)
    content = StringField()
    date = DateTimeField(required=True)
