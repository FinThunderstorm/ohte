import unittest
from freezegun import freeze_time
from utils.helpers import get_time, get_test_user, get_id
from repositories.UserRepository import UserRepository


@freeze_time(get_time())
class TestMemoRepository(unittest.TestCase):

    def setUp(self):
        self.userrepo = UserRepository(prod=False)

    def test_count_all_users(self):
        before = self.userrepo.count_all_users()
        self.userrepo.new_user(get_test_user())
        self.assertEqual(self.userrepo.count_all_users(), before + 1)

    def test_get_all_users_works(self):
        before = self.userrepo.count_all_users()
        for i in range(before+1, before+4):
            self.userrepo.new_user(get_test_user(i))
        all_users = self.userrepo.get_all_users()
        self.assertEqual(len(all_users), before+3)
        for user in all_users:
            self.assertEqual(user.firstname, get_test_user()["firstname"])

    def test_new_user_returns_new_user(self):
        for user in self.userrepo.get_all_users():
            print(user.id, user.username)
        user = get_test_user(self.userrepo.count_all_users() + 1)
        print(user["username"])
        saved_user = self.userrepo.new_user(user)
        self.assertIsNotNone(saved_user.id)

    def test_new_user_with_existing_username_returns_none(self):
        user1 = get_test_user(self.userrepo.count_all_users() + 1)
        user2 = get_test_user(self.userrepo.count_all_users())
        self.userrepo.new_user(user1)
        saved_user2 = self.userrepo.new_user(user2)
        self.assertIsNone(saved_user2)

    def test_login_with_right_credentials_returns_user(self):
        user = get_test_user(self.userrepo.count_all_users() + 1)
        saved_user = self.userrepo.new_user(user)
        logged_user = self.userrepo.login(user["username"], user["password"])
        self.assertEqual(logged_user.id, saved_user.id)
        self.assertEqual(logged_user.username, saved_user.username)

    def test_login_with_wrong_credentials_returns_none(self):
        user = get_test_user(self.userrepo.count_all_users() + 1)
        saved_user = self.userrepo.new_user(user)
        logged_user_w_pw = self.userrepo.login(user["username"], "wrong")
        logged_user_w_un = self.userrepo.login("wrong", user["password"])
        logged_user_w_pw_un = self.userrepo.login("wrong", "wrong")
        self.assertIsNone(logged_user_w_pw)
        self.assertIsNone(logged_user_w_un)
        self.assertIsNone(logged_user_w_pw_un)

    def test_find_one_user_with_username(self):
        user = get_test_user(self.userrepo.count_all_users()+1)
        saved_user = self.userrepo.new_user(user)
        queried_user = self.userrepo.find_one_user(
            "username", saved_user.username)
        self.assertEqual(queried_user, saved_user)
        self.assertEqual(queried_user.username, saved_user.username)

    def test_find_one_user_with_id(self):
        user = get_test_user(self.userrepo.count_all_users()+1)
        saved_user = self.userrepo.new_user(user)
        queried_user = self.userrepo.find_one_user("id", saved_user.id)
        self.assertEqual(queried_user, saved_user)
        self.assertEqual(queried_user.id, saved_user.id)

    def test_update_user_really_changes(self):
        user = get_test_user(self.userrepo.count_all_users() + 1)
        saved_user = self.userrepo.new_user(user)
        saved_user.firstname = "Updated"
        self.userrepo.update_user(saved_user)
        queried_user = self.userrepo.find_one_user("id", saved_user.id)
        self.assertEqual(queried_user.firstname, saved_user.firstname)
        self.assertEqual(queried_user.id, saved_user.id)

    def test_remove_user_works_valid_id(self):
        user = get_test_user(self.userrepo.count_all_users() + 1)
        saved_user = self.userrepo.new_user(user)
        remove_result = self.userrepo.remove_user(saved_user.id)
        self.assertTrue(remove_result)

    def test_remove_user_returns_false_non_valid_id(self):
        remove_result = self.userrepo.remove_user(get_id())
        self.assertFalse(remove_result)
