from mongoengine import Document, StringField, ReferenceField, IntField


class Image(Document):
    """Class for image objects. Inherits from mongonengines document class
    by giving all functions from that. Class defines types for database.

    author is required reference to User, when object is got from database, is replaced
    with user object. Holds information of image's author.

    name is required string, limited length 50 characters. Holds name for image.

    image is required string, code should be saving image content as base64 encoded.

    filetype is required string, holds images filetype.

    width is int, used for rendering images in MemoView.
    """
    author = ReferenceField('User', required=True)
    name = StringField(required=True, max_length=50)
    image = StringField(required=True)
    filetype = StringField(required=True)
    width = IntField()
