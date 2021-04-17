from bson.objectid import ObjectId
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime
from entities.user import User
from entities.memo import Memo


def get_time():
    return datetime.utcnow()


def get_test_memo_user():
    user = User(
        id=get_id('6072d33e3a3c627a49901ce8'),
        firstname="Memo",
        lastname="User",
        username="memouser",
        password="$2b$12$1kt3hr6qYP4HPG5pdGZwHOW8QrYhZW79hpTbS2Ouw.oxr2pO9BYyG",
    )
    return user


def get_test_memo(index=None):
    memo = {
        "author": get_test_memo_user(),
        "title": "Test Memo",
        "content": "Lorem ipsum dolor sit amet.",
        "date": get_time(),
    }
    if index:
        memo["title"] = "Test Memo " + str(index)
    return memo


def get_test_memo_obj():
    memo = Memo(
        author=get_test_memo_user(),
        title="not",
        content="valid",
        date=get_time(),
    )
    return memo


def get_test_user(index=None):
    user = {
        "firstname": "Test",
        "lastname": "User" if not index else "User"+str(index),
        "username": "testuser"+str(index),
        "password": "password",
    }
    return user


def get_type_id():
    return type(get_id())


def get_type_user():
    return type(get_test_memo_user())


def get_type_memo():
    return type(get_test_memo_obj())


def generate_password_hash(password):
    salt = gensalt()
    password_hash = hashpw(bytes(password, 'utf-8'), salt)
    return password_hash


def check_password(password, hashed_password):
    result = checkpw(password, hashed_password)
    return result


def get_id(sid=None):
    return ObjectId(sid)
