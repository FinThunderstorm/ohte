from datetime import datetime
from bson.objectid import ObjectId
from bcrypt import gensalt, hashpw, checkpw
from entities.user import User
from entities.memo import Memo


def get_time():
    return datetime.utcnow()


def get_time_timestamp(year, month, day, hours, minutes, seconds):
    return datetime(year, month, day, hours, minutes, seconds)


def get_test_memo_user(uid="6072d33e3a3c627a49901ce8", username="memouser"):
    user = User(
        id=get_id(uid),
        firstname="Memo",
        lastname="User",
        username=username,
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


def get_test_user_obj(uid="6072d33e3a3c627a49901ce8", username="memouser"):
    return get_test_memo_user(uid, username)


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
        "real_password": "password",
        "password": "$2b$12$1kt3hr6qYP4HPG5pdGZwHOW8QrYhZW79hpTbS2Ouw.oxr2pO9BYyG"
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
    result = checkpw(bytes(password, 'utf-8'), bytes(hashed_password, 'utf-8'))
    return result


def get_id(sid=None):
    return ObjectId(sid)


def get_empty_memo():
    return Memo(
        author=get_test_memo_user(),
        title="",
        content="",
        date=get_time(),
    )
