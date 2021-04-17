import unittest
from freezegun import freeze_time
from utils.database_handler import connect_test_database, disconnect_database
from utils.helpers import get_time, get_id, get_test_user
from services.memo_service import memo_service
from services.user_service import user_service


@freeze_time(get_time())
class TestUserService(unittest.TestCase):
    def setUp(self):
        connect_test_database()
        self.user_service = user_service
        self.memo_service = memo_service
        self.before = self.user_service.count()
        self.test_user = get_test_user()
        self.saved_user = self.memo_service.create(
            self.test_user["firstname"],
            self.test_user["lastname"],
            self.test_user["username"],
            self.test_user["password"],
        )

    def tearDown(self):
        disconnect_database()
