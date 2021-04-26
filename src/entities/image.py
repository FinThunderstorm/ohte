from mongoengine import Document, StringField, ReferenceField, IntField


class Image(Document):
    author = ReferenceField('User', required=True)
    name = StringField(required=True, max_length=50)
    image = StringField(required=True)
    filetype = StringField(required=True)
    width = IntField()
