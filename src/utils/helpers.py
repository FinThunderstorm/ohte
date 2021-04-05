from bson.objectid import ObjectId
from bcrypt import gensalt, hashpw, checkpw
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


def get_test_user(index=None):
    user = {
        "firstname": "Test",
        "lastname": "User" if not index else "User"+str(index),
        "username": "testuser"+str(index),
        "password": "password",
    }
    return user


def generate_password_hash(password):
    salt = gensalt()
    password_hash = hashpw(bytes(password, 'utf-8'), salt)
    return password_hash


def check_password(password, hashed_password):
    result = checkpw(password, hashed_password)
    return result


def get_id(sid=None):
    return ObjectId(sid)
