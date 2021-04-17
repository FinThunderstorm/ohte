import unittest
from freezegun import freeze_time
from entities.user import User

from utils.helpers import get_time, get_test_user


@freeze_time(get_time())
class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = get_test_user()
        self.new_user = User(firstname=self.user["firstname"],
                             lastname=self.user["lastname"],
                             username=self.user["username"],
                             password=self.user["password"])

    def test_user_initializes(self):
        self.assertEqual(self.new_user.firstname, self.user["firstname"])
        self.assertEqual(self.new_user.lastname, self.user["lastname"])
        self.assertEqual(self.new_user.username, self.user["username"])
        self.assertEqual(self.new_user.password, self.user["password"])
