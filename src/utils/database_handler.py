from mongoengine import connect, disconnect, ConnectionFailure
from pymongo.errors import ConfigurationError


def connect_database(db_uri):
    try:
        return connect(host=db_uri)
    except ConnectionFailure:
        return None
    except ConfigurationError:
        return None


def connect_test_database(db_uri='mongomock://localhost'):
    return connect_database(db_uri)


def disconnect_database():
    return disconnect()
