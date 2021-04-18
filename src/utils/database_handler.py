from mongoengine import connect, disconnect, ConnectionFailure
from pymongo.errors import ConfigurationError
from utils.config import database_uri


def connect_database(db_uri=database_uri):
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
