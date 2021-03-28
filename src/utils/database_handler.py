from mongoengine import connect
from utils.config import database_uri


def connect_database(prod=True):
    return connect(host=database_uri) if prod else connect(host='mongomock://localhost')
