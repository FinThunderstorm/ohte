from bson.objectid import ObjectId
from datetime import datetime


def get_time():
    return datetime.utcnow()


def get_test_memo(index=None):
    memo = {
        "author_id": ObjectId(),
        "title": "Test Memo",
        "content": "Lorem ipsum dolor sit amet.",
        "date": get_time(),
    }
    if index:
        memo["title"] = "Test Memo " + str(index)
    return memo


def get_id(sid=None):
    return ObjectId(sid)
