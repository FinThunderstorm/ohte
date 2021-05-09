from datetime import datetime
from bson.objectid import ObjectId
from bson.errors import InvalidId
from bcrypt import gensalt, hashpw, checkpw
from entities.user import User
from entities.memo import Memo
from entities.image import Image


def get_time():
    """get_time is used for getting datetime-object.

    Returns:
        DateTime: returns DateTime-object with current UTC-time.
    """
    return datetime.utcnow()


def get_time_timestamp(year, month, day, hours, minutes, seconds):
    """get_time_timestamp is used for creating DateTime with exact days.
    Mainly used for testing purposes.

    Args:
        year: given year for object
        month: given month for object
        day: given day for object
        hours: given hours for object
        minutes: given minutes for object
        seconds: given seconds for object

    Returns:
        DateTime: DateTime object with given args.
    """
    return datetime(year, month, day, hours, minutes, seconds)


def get_test_memo_user(uid="6072d33e3a3c627a49901ce8", username="memouser"):
    """get_test_memo_user is used for mocking User objects with values. Mainly used with tests.

    Args:
        uid: Optional value to mock user with specific id. Defaults to "6072d33e3a3c627a49901ce8".
        username: Optional value to mock user with specific username. Defaults to "memouser".

    Returns:
        User: created User-object.
    """
    user = User(
        id=get_id(uid),
        firstname="Memo",
        lastname="User",
        username=username,
        password="$2b$12$1kt3hr6qYP4HPG5pdGZwHOW8QrYhZW79hpTbS2Ouw.oxr2pO9BYyG",
    )
    return user


def get_test_memo(index=None):
    """get_test_memo is used for creating Memos and getting base values.
    Mainly used with tests.

    Args:
        index: Optional value to mock memo with different titles. Defaults to None.

    Returns:
        dict: dictionary with values suitable for testing.
    """
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
    """get_test_user_obj is alternative call for testing.

    Args:
        uid: Optional value to mock user with specific id. Defaults to "6072d33e3a3c627a49901ce8".
        username: Optional value to mock user with specific username. Defaults to "memouser".

    Returns:
        User: created User-object.
    """
    return get_test_memo_user(uid, username)


def get_test_memo_obj():
    """get_test_memo_obj is used for mocking Memo objects with values. Mainly used with tests.

    Returns:
        Memo: created Memo-object.
    """
    memo = Memo(
        author=get_test_memo_user(),
        title="not",
        content="valid",
        date=get_time(),
    )
    return memo


def get_test_image_obj():
    """get_test_image_obj is used for mocking Memo objects with values. Mainly used with tests.

    Returns:
        Memo: created Memo-object.
    """
    image = Image(
        author=get_test_memo_user(),
        name="Test Image",
        image="unvalid image base64 encoding",
    )
    return image


def get_test_user(index=None):
    """get_test_memo is used for creating Memos and getting base values.
    Mainly used with tests.

    Args:
        index: Optional value to mock memo with different titles. Defaults to None.

    Returns:
        dict: dictionary with values suitable for testing.
    """
    user = {
        "firstname": "Test",
        "lastname": "User" if not index else "User"+str(index),
        "username": "testuser"+str(index),
        "real_password": "password",
        "password": "$2b$12$1kt3hr6qYP4HPG5pdGZwHOW8QrYhZW79hpTbS2Ouw.oxr2pO9BYyG"
    }
    return user


def get_type_id():
    """get_type_id returns type data of ObjectId for checking
    if item is right instance.

    Returns:
        type: holds type value of ObjectId
    """
    return type(get_id())


def get_type_user():
    """get_type_user returns type data of User for checking
    if item is right instance.

    Returns:
        type: holds type value of User
    """
    return type(get_test_memo_user())


def get_type_memo():
    """get_type_memo returns type data of Memo for checking
    if item is right instance.

    Returns:
        type: holds type value of Memo
    """
    return type(get_test_memo_obj())


def get_type_image():
    """get_type_id returns type data of Image for checking
    if item is right instance.

    Returns:
        type: holds type value of Image
    """
    return type(get_test_image_obj())


def generate_password_hash(password):
    """generate_password_hash is used for making passsword
    hash to save passwords as encrypted form factor into
    database. Using bcrypt.

    Args:
        password: password string as plain text

    Returns:
        str: password string as hashed version
    """
    salt = gensalt()
    password_hash = hashpw(bytes(password, 'utf-8'), salt)
    return password_hash


def check_password(password, hashed_password):
    """check_password is used to check if plain text password and hashed
    password are matching each other.

    Args:
        password: given password as plain text
        hashed_password: password hash for comparation

    Returns:
        bool: were password correct or not.
    """
    result = checkpw(bytes(password, 'utf-8'), bytes(hashed_password, 'utf-8'))
    return result


def get_id(sid=None):
    """get_id is used for converting id from string into ObjectId used
    by database.

    Args:
        sid: optional string argument for getting ObjectId for
        specific id. Defaults to None.

    Returns:
        Union(ObjectId, None): if no seed id given or valid seed id given,
                               returns ObjectId, else None.
    """
    try:
        return ObjectId(sid)
    except InvalidId:
        return None


def get_empty_memo():
    """get_empty_memo is used for mocking Memo object to initialize app with
    no information. Main purpose is to have object with all attributes
    such as id.

    Returns:
        Memo: Memo object with mocked attributes.
    """
    return Memo(
        id=get_id("6072d33e3a3c627a49901ce8"),
        author=get_test_memo_user(),
        title="",
        content="",
        date=get_time(),
    )
