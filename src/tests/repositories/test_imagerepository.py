import unittest
from repositories.image_repository import image_repository
from utils.helpers import get_id, get_test_image_obj
from utils.database_handler import connect_test_database, disconnect_database


class TestImageRepository(unittest.TestCase):
    def setUp(self):
        self.imagerepo = image_repository
        connect_test_database()

    def tearDown(self):
        disconnect_database()

    def test_remove_unvalid_id(self):
        image = get_test_image_obj()
        image.id = get_id()
        res = self.imagerepo.remove(image)
        self.assertFalse(res)
