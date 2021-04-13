import unittest
from freezegun import freeze_time
from utils.helpers import get_time, get_test_user, get_id
from utils.database_handler import connect_database, disconnect_database
from repositories.UserRepository import user_repository


@freeze_time(get_time())
class TestUserRepository(unittest.TestCase):

    def setUp(self):
        connect_database(prod=False)
        self.userrepo = user_repository
        self.before = self.userrepo.count()
        self.test_user = get_test_user(self.before+1)
        self.saved_user = self.userrepo.new(self.test_user)

    def tearDown(self):
        disconnect_database()

    def test_count_all_users(self):
        before = self.userrepo.count()
        self.userrepo.new(get_test_user())
        self.assertEqual(self.userrepo.count(), before + 1)

    def test_get_all_users_works(self):
        for i in range(self.before+1, self.before+4):
            self.userrepo.new(get_test_user(i))
        all_users = self.userrepo.get()
        self.assertEqual(len(all_users), self.before+3)
        for user in all_users:
            self.assertEqual(user.firstname, get_test_user()["firstname"])

    def test_new_user_returns_new_user(self):
        self.assertIsNotNone(self.saved_user.id)

    def test_new_user_with_existing_username_returns_none(self):
        dublicate_user = get_test_user(self.userrepo.count())
        saved_dublicate_user = self.userrepo.new(dublicate_user)
        self.assertIsNone(saved_dublicate_user)

    def test_login_with_right_credentials_returns_user(self):
        logged_user = self.userrepo.login(
            self.test_user["username"], self.test_user["password"])
        self.assertEqual(logged_user.id, self.saved_user.id)
        self.assertEqual(logged_user.username, self.saved_user.username)

    def test_login_with_wrong_credentials_returns_none(self):
        logged_user_w_pw = self.userrepo.login(
            self.test_user["username"], "wrong")
        logged_user_w_un = self.userrepo.login(
            "wrong", self.test_user["password"])
        logged_user_w_pw_un = self.userrepo.login("wrong", "wrong")
        self.assertIsNone(logged_user_w_pw)
        self.assertIsNone(logged_user_w_un)
        self.assertIsNone(logged_user_w_pw_un)

    def test_find_one_user_with_username(self):
        queried_user = self.userrepo.get(
            "username", self.saved_user.username)
        self.assertEqual(queried_user, self.saved_user)
        self.assertEqual(queried_user.username, self.saved_user.username)

    def test_find_one_user_with_id(self):
        queried_user = self.userrepo.get("id", self.saved_user.id)
        self.assertEqual(queried_user, self.saved_user)
        self.assertEqual(queried_user.id, self.saved_user.id)

    # def test_update_user_really_changes(self):
    #     self.saved_user.firstname = "Updated"
    #     self.userrepo.update_user(self.saved_user)
    #     queried_user = self.userrepo.get("id", self.saved_user.id)
    #     self.assertEqual(queried_user.firstname, self.saved_user.firstname)
    #     self.assertEqual(queried_user.id, self.saved_user.id)

    # def test_remove_user_works_valid_id(self):
    #     remove_result = self.userrepo.remove(self.saved_user.id)
    #     self.assertTrue(remove_result)

    def test_remove_user_returns_false_non_valid_id(self):
        remove_result = self.userrepo.remove(get_id())
        self.assertFalse(remove_result)
