import unittest
from freezegun import freeze_time
from utils.database_handler import connect_test_database, disconnect_database
from utils.helpers import get_time, get_time_timestamp, get_test_memo, get_id, get_test_memo_user, get_test_user_obj
from services.image_service import image_service
from repositories.user_repository import user_repository


@freeze_time(get_time())
class TestImageService(unittest.TestCase):
    def setUp(self):
        connect_test_database()

    def tearDown(self):
        disconnect_database()

    # create
    def test_create_returns_new_memo_with_all_attributes(self):
        print('toot')
