from mongoengine import connect, disconnect, ConnectionFailure
from pymongo.errors import ConfigurationError


def connect_database(db_uri):
    """connect_database is used for initializing connection to
    MongoDB-database.

    Args:
        db_uri: address to external MongoDB-database

    Returns:
        Union(MongoClient,None): if connection is successful, returns mongoclient
                                 to show established connection, if problems,
                                 returns None.
    """
    try:
        conn = connect(host=db_uri)
        return conn
    except ConnectionFailure:
        return None
    except ConfigurationError:
        return None


def connect_test_database():
    """connect_database is used in tests to connect into database,
    returns connection to test database using connect_database.

    Returns:
        Union(MongoClient,None): if connection is successful, returns mongoclient
                                 to show established connection, if problems,
                                 returns None.
    """
    db_uri = 'mongomock://localhost'
    return connect_database(db_uri)


def disconnect_database():
    """disconnect_database removes current connection into database.
    """
    disconnect()
