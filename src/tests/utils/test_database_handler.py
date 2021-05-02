import unittest
from mongoengine import ConnectionFailure
from pymongo.errors import ConfigurationError
from utils.config import Config
from utils.database_handler import connect_database, connect_test_database, disconnect_database
from services.file_service import file_service


class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.config = Config(file_service)

    def tearDown(self):
        disconnect_database()

    # def test_connect_database_with_valid_url_works(self):
    #     conn = connect_database('mongomock://localhost')
    #     self.assertIsNotNone(conn)

    # def test_connect_database_raises_connectionfailure_when_no_internet(self):
    #     conn = connect_database(database_uri)
    #     self.assertIsNone(conn)
    #     self.assertRaises(ConnectionFailure)

    # def test_connect_database_raises_configurationerror_when_not_valid_db_uri(self):
    #     conn = connect_database(
    #         'mongodb+srv://username:password@xxxxx.yyy.zzz.osoite.fi/muistio?retryWrites=true&w=majority')
    #     self.assertRaises(ConfigurationError)

    # def test_connect_test_database_works(self):
    #     conn = connect_test_database()
    #     self.assertIsNotNone(conn)
