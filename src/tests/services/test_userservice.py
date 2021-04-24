import unittest
from freezegun import freeze_time
from utils.database_handler import connect_test_database, disconnect_database
from utils.helpers import get_time, get_id, get_test_user, get_type_user
from services.memo_service import memo_service
from services.user_service import user_service


@freeze_time(get_time())
class TestUserService(unittest.TestCase):
    def setUp(self):
        connect_test_database()
        self.user_service = user_service
        self.memo_service = memo_service
        self.before = self.user_service.count()
        self.test_user = get_test_user(0)

        self.saved_user = self.user_service.create(
            self.test_user["firstname"],
            self.test_user["lastname"],
            self.test_user["username"],
            "password",
        )

    def tearDown(self):
        disconnect_database()

    # create
    def test_create_with_valid_works(self):
        self.assertIsNotNone(self.saved_user)
        self.assertIsInstance(self.saved_user, get_type_user())
        self.assertEqual(self.saved_user.firstname,
                         self.test_user["firstname"])
        self.assertEqual(self.saved_user.firstname,
                         self.test_user["firstname"])
        self.assertEqual(self.saved_user.firstname,
                         self.test_user["firstname"])
        self.assertIsNotNone(self.saved_user.password)
        self.assertIsNotNone(self.saved_user.memos)

    def test_create_with_duplicate_username_returns_none(self):
        second_saved_user = self.user_service.create(
            self.test_user["firstname"],
            self.test_user["lastname"],
            self.test_user["username"],
            "password",
        )
        self.assertIsNone(second_saved_user)

    def test_create_user_as_empty_reutrns_none(self):
        result = self.user_service.create("", "", "", "")
        self.assertIsNone(result)

    # update
    def test_update_changes_values(self):
        firstname = "Changed"
        lastname = "Cool-Name"
        password = "nönnönnöö123?"

        updated_user = self.user_service.update(
            self.saved_user.id, firstname, lastname, self.saved_user.username, password)

        self.assertIsNotNone(updated_user)
        self.assertIsInstance(updated_user, get_type_user())
        self.assertEqual(updated_user.id, self.saved_user.id)
        self.assertEqual(updated_user.firstname, firstname)
        self.assertEqual(updated_user.lastname, lastname)
        self.assertEqual(updated_user.username, self.saved_user.username)
        self.assertIsNotNone(updated_user.password)
        self.assertNotEqual(updated_user.password, password)
        self.assertNotEqual(updated_user.password, self.saved_user.password)
        self.assertEqual(updated_user.memos, self.saved_user.memos)

    def test_update_duplicate_username_returns_none(self):
        test_user = get_test_user(2)
        self.user_service.create(
            test_user["firstname"],
            test_user["lastname"],
            test_user["username"],
            test_user["password"],
        )

        updated_user = self.user_service.update(
            self.saved_user.id, self.saved_user.firstname, self.saved_user.lastname, test_user[
                "username"], self.saved_user.password)
        self.assertIsNone(updated_user)

    # remove

    def test_remove_removes_valid_user(self):
        user_id = self.saved_user.id
        before = self.user_service.count()
        result = self.user_service.remove(user_id)
        after = self.user_service.count()
        query = self.user_service.get('id', user_id)
        self.assertTrue(result)
        self.assertIsNone(query)
        self.assertEqual(after, before - 1)

    def test_remove_returns_false_with_unvalid_id(self):
        before = self.user_service.count()
        result = self.user_service.remove(get_id())
        after = self.user_service.count()
        self.assertFalse(result)
        self.assertEqual(after, before)

    # get
    def test_get_defaults_to_all(self):
        for i in range(1, 4):
            user = get_test_user(i)
            self.user_service.create(
                user["firstname"], user["lastname"], user["username"], user["password"])
        count = self.user_service.count()
        users = self.user_service.get()
        self.assertEqual(len(users), count)

    def test_get_all_works(self):
        added_users = []
        added_users.append(self.saved_user)
        for i in range(1, 4):
            user = get_test_user(i)
            added = self.user_service.create(
                user["firstname"], user["lastname"], user["username"], user["password"])
            added_users.append(added)
        users = self.user_service.get()
        print(len(users), len(added_users))
        for i in range(len(users)):
            self.assertEqual(users[i], added_users[i])

    def test_get_username_returns_only_one(self):
        queried_user = self.user_service.get(
            "username", self.saved_user.username)
        self.assertIsInstance(queried_user, get_type_user())
        self.assertEqual(queried_user, self.saved_user)
        self.assertEqual(queried_user.id, self.saved_user.id)
        self.assertEqual(queried_user.username, self.saved_user.username)

    def test_get_unvalid_username_returns_none(self):
        queried_user = self.user_service.get("username", "notvalid")
        self.assertIsNone(queried_user)

    def test_get_id_returns_only_one(self):
        queried_user = self.user_service.get("id", self.saved_user.id)
        self.assertIsInstance(queried_user, get_type_user())
        self.assertEqual(queried_user, self.saved_user)
        self.assertEqual(queried_user.id, self.saved_user.id)
        self.assertEqual(queried_user.username, self.saved_user.username)

    def test_get_unvalid_id_returns_none(self):
        queried_user = self.user_service.get("id", get_id())
        self.assertIsNone(queried_user)

    # count
    def test_count_defaults_to_all(self):
        for i in range(1, 4):
            user = get_test_user(i)
            self.user_service.create(
                user["firstname"], user["lastname"], user["username"], user["password"])
        users = self.user_service.get()
        count = self.user_service.count()
        self.assertEqual(count, len(users))

    def test_count_all_works(self):
        before = self.user_service.count('all')
        user = get_test_user(2)
        self.user_service.create(
            user["firstname"], user["lastname"], user["username"], user["password"])
        after = self.user_service.count('all')
        self.assertEqual(after, before + 1)

    def test_count_all_with_multiple_users_works(self):
        before = self.user_service.count('all')
        for i in range(1, 4):
            user = get_test_user(i)
            self.user_service.create(
                user["firstname"], user["lastname"], user["username"], user["password"])
        after = self.user_service.count('all')
        self.assertEqual(after, before + 3)

    def test_count_username_returns_only_one(self):
        result = self.user_service.count('username', self.saved_user.username)
        self.assertEqual(result, 1)

    def test_count_unvalid_username_returns_zero(self):
        result = self.user_service.count('username', "notvalid")
        self.assertEqual(result, 0)

    def test_count_id_returns_only_one(self):
        result = self.user_service.count('id', self.saved_user.id)
        self.assertEqual(result, 1)

    def test_count_unvalid_id_returns_zero(self):
        result = self.user_service.count('id', get_id())
        self.assertEqual(result, 0)

    # login
    def test_login_with_correct_credentials_works(self):
        login = self.user_service.login(self.saved_user.username, "password")
        self.assertIsInstance(login, get_type_user())
        self.assertEqual(login, self.saved_user)
        self.assertEqual(login.id, self.saved_user.id)
        self.assertEqual(login.username, self.saved_user.username)

    def test_login_with_unvalid_username_returns_none(self):
        login = self.user_service.login("notvalid", "password")
        self.assertIsNone(login)

    def test_login_with_unvalid_password_returns_none(self):
        login = self.user_service.login(self.saved_user.username, "notvalid")
        self.assertIsNone(login)

    def test_login_with_unvalid_username_and_password_returns_none(self):
        login = self.user_service.login("notvalid", "notvalid")
        self.assertIsNone(login)
