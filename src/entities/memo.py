from bson.objectid import ObjectId
from datetime import datetime


class Memo:
    def __init__(self, author_id, title="", content="", obj_id=ObjectId()):
        self.id = obj_id
        self.title = title if title != "" else "Memo " + \
            str(datetime.utcnow().isoformat())
        self.content = content
        self.author_id = author_id
        self.date = datetime.utcnow()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "date": self.date,
        }
