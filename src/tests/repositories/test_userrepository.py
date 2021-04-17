import unittest
from freezegun import freeze_time
from utils.helpers import get_time, get_test_user, get_test_user_obj, get_id
from utils.database_handler import connect_test_database, disconnect_database
from repositories.UserRepository import user_repository


@freeze_time(get_time())
class TestUserRepository(unittest.TestCase):

    def setUp(self):
        connect_test_database()
        self.userrepo = user_repository
        self.before = self.userrepo.count()
        self.test_user = get_test_user(self.before + 1)  # was + 1
        self.saved_user = self.userrepo.new(self.test_user)

    def tearDown(self):
        disconnect_database()

    # count
    def test_count_defaults_to_all_users(self):
        for i in range(self.before+1, self.before+4):
            self.userrepo.new(get_test_user(i))
        count = self.userrepo.count()
        users = self.userrepo.get()
        self.assertEqual(count, len(users))

    def test_count_all_users(self):
        before = self.userrepo.count('all')
        self.userrepo.new(get_test_user())
        self.assertEqual(self.userrepo.count('all'), before + 1)

    def test_count_all_with_multiple_added_works(self):
        for i in range(self.before + 1, self.before + 4):
            self.userrepo.new(get_test_user(i))
        count = self.userrepo.count('all')
        users = self.userrepo.get()
        self.assertEqual(count, len(users))

    def test_count_id_returns_only_one(self):
        result = self.userrepo.count('id', self.saved_user.id)
        self.assertEqual(result, 1)

    def test_count_not_valid_id_returns_zero(self):
        result = self.userrepo.count('id', get_id())
        self.assertEqual(result, 0)

    def test_count_username_returns_only_one(self):
        result = self.userrepo.count('username', self.saved_user.username)
        self.assertEqual(result, 1)

    def test_count_not_valid_username_returns_zero(self):
        result = self.userrepo.count('username', "nonnnonnoo")
        self.assertEqual(result, 0)

    # new
    def test_new_user_returns_new_user(self):
        self.assertIsNotNone(self.saved_user.id)
        self.assertEqual(self.saved_user.firstname,
                         self.test_user["firstname"])
        self.assertEqual(self.saved_user.lastname,
                         self.test_user["lastname"])
        self.assertEqual(self.saved_user.username,
                         self.test_user["username"])
        self.assertIsNotNone(self.saved_user.memos)

    def test_new_user_with_existing_username_returns_none(self):
        duplicate_user = get_test_user(self.userrepo.count())
        saved_duplicate_user = self.userrepo.new(duplicate_user)
        self.assertIsNone(saved_duplicate_user)

    # update

    def test_update_user_changes_values(self):
        self.saved_user.firstname = "Updated"
        updated_user = self.userrepo.update(self.saved_user)
        self.assertEqual(updated_user.firstname, self.saved_user.firstname)
        self.assertEqual(updated_user.lastname, self.saved_user.lastname)
        self.assertEqual(updated_user.username, self.saved_user.username)
        self.assertEqual(updated_user.password, self.saved_user.password)
        self.assertEqual(updated_user.id, self.saved_user.id)

    def test_update_user_makes_changes_to_db(self):
        self.saved_user.firstname = "Updated"
        self.userrepo.update(self.saved_user)
        queried_user = self.userrepo.get("id", self.saved_user.id)
        self.assertEqual(queried_user.firstname, self.saved_user.firstname)
        self.assertEqual(queried_user.lastname, self.saved_user.lastname)
        self.assertEqual(queried_user.username, self.saved_user.username)
        self.assertEqual(queried_user.password, self.saved_user.password)
        self.assertEqual(queried_user.id, self.saved_user.id)

    # remove
    def test_remove_user_works_valid_user(self):
        before = self.userrepo.count()
        remove_result = self.userrepo.remove(self.saved_user)
        after = self.userrepo.count()
        self.assertTrue(remove_result)
        self.assertEqual(after, before-1)

    def test_remove_user_returns_false_non_valid_user(self):
        before = self.userrepo.count()
        remove_result = self.userrepo.remove(
            get_test_user_obj("6072d33e3a3c627a49901cd7", "notvalid"))
        after = self.userrepo.count()
        self.assertFalse(remove_result)
        self.assertEqual(after, before)

    # get
    def test_get_defaults_get_all(self):
        for i in range(self.before+1, self.before+4):
            self.userrepo.new(get_test_user(i))
        count = self.userrepo.count()
        users = self.userrepo.get()
        self.assertEqual(len(users), count)

    def test_get_all_works(self):
        for i in range(self.before+1, self.before+4):
            self.userrepo.new(get_test_user(i))
        all_users = self.userrepo.get()
        self.assertEqual(len(all_users), self.before+3)
        for user in all_users:
            self.assertEqual(user.firstname, get_test_user()["firstname"])

    def test_get_username_works(self):
        queried_user = self.userrepo.get(
            "username", self.saved_user.username)
        self.assertEqual(queried_user, self.saved_user)
        self.assertEqual(queried_user.username, self.saved_user.username)

    def test_get_id_works(self):
        queried_user = self.userrepo.get("id", self.saved_user.id)
        self.assertEqual(queried_user, self.saved_user)
        self.assertEqual(queried_user.id, self.saved_user.id)
