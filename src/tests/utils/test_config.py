from os import path, remove
import unittest
from services.file_service import file_service
from utils.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.file_service = file_service
        self.src = path.join(path.dirname(__file__), '..',
                             './testdata', '.env.test')
        self.src = path.normpath(self.src)
        self.config = Config(self.file_service, self.src)

    def test_initialize_premade_config_works(self):
        src = path.join(path.dirname(__file__), '..',
                        './testdata', '.env.test')
        src = path.normpath(src)
        config = Config(file_service, src)

        self.assertFalse(config.initialized_first_time)
        self.assertIsNotNone(config.get_all())

    def test_initialize_without_previous_config_works(self):
        src = path.join(path.dirname(__file__), '..',
                        './testdata', '.env.notexists')
        src = path.normpath(src)
        config = Config(file_service, src)

        configs = config.get_all()
        self.assertTrue(config.initialized_first_time)
        self.assertIsNotNone(configs)
        self.assertEqual(configs["RES_INDEX"], 0)
        self.assertEqual(configs["DB_NAME"], "muistio")

    def test_get_setting_works(self):
        self.assertEqual(self.config.get('RES_INDEX'), "5")
        self.assertEqual(self.config.get('RES_FORMAT'), "1650x1050")
        self.assertEqual(self.config.get('DB_USERNAME'), "test")
        self.assertEqual(self.config.get('DB_PASSWORD'), "test")
        self.assertEqual(self.config.get('DB_SERVER'),
                         "ohte.bu0r9.mongodb.net")
        self.assertEqual(self.config.get('DB_NAME'), "muistio")
        self.assertIsNotNone(self.config.get('DATABASE_URI'))

    def test_get_all_works(self):
        configs = {}
        configs["RES_INDEX"] = "5"
        configs["RES_FORMAT"] = "1650x1050"
        configs["DB_USERNAME"] = "test"
        configs["DB_PASSWORD"] = "test"
        configs["DB_SERVER"] = "ohte.bu0r9.mongodb.net"
        configs["DB_NAME"] = "muistio"
        configs["DATABASE_URI"] = "mongodb+srv://test:test" \
            + "@ohte.bu0r9.mongodb.net/muistio?retryWrites=true&w=majority"

        self.assertEqual(self.config.get_all(), configs)

    def test_set_value_works(self):
        self.config.set_value('RES_INDEX', '1')
        self.config.set_value('RES_FORMAT', "auto")
        self.assertEqual(self.config.get('RES_INDEX'), "1")
        self.assertEqual(self.config.get('RES_FORMAT'), "auto")

    def test_set_empty_value_raises_value_error(self):
        try:
            self.config.set_value('RES_INDEX', '')
        except ValueError as error:
            self.assertRaises(ValueError)
            self.assertEqual(error.args[0], "Value can not be empty")

    def test_save_works(self):
        src = path.join(path.dirname(__file__), '..',
                        './testdata', '.env.changes')
        src = path.normpath(src)
        config = Config(file_service, src)

        self.assertEqual(config.get('RES_INDEX'), 0)
        self.assertEqual(config.get('RES_FORMAT'), "")
        self.assertEqual(config.get('DB_USERNAME'), "")
        self.assertEqual(config.get('DB_PASSWORD'), "")
        self.assertEqual(config.get('DB_SERVER'),
                         "ohte.bu0r9.mongodb.net")
        self.assertEqual(config.get('DB_NAME'), "muistio")
        self.assertIsNotNone(config.get('DATABASE_URI'))

        config.set_value('RES_INDEX', "1")
        config.set_value('RES_FORMAT', 'auto')
        config.set_value('DB_USERNAME', "username")
        config.set_value('DB_PASSWORD', "password")

        config.save()

        configs = {}
        configs["RES_INDEX"] = "1"
        configs["RES_FORMAT"] = "auto"
        configs["DB_USERNAME"] = "username"
        configs["DB_PASSWORD"] = "password"
        configs["DB_SERVER"] = "ohte.bu0r9.mongodb.net"
        configs["DB_NAME"] = "muistio"
        configs["DATABASE_URI"] = "mongodb+srv://username:password" \
            + "@ohte.bu0r9.mongodb.net/muistio?retryWrites=true&w=majority"

        self.assertEqual(config.get_all(), configs)

        remove(src)
