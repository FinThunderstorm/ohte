import unittest
from freezegun import freeze_time
from utils.helpers import get_time, get_test_memo, get_test_memo_user, get_id, get_test_memo_obj
from utils.database_handler import connect_test_database, disconnect_database
from repositories.memo_repository import memo_repository
from repositories.user_repository import user_repository


@freeze_time(get_time())
class TestMemoRepository(unittest.TestCase):

    def setUp(self):
        connect_test_database()
        self.userrepo = user_repository
        self.user = self.userrepo.update(get_test_memo_user())
        self.user_two = self.userrepo.update(
            get_test_memo_user("6072d33e3a3c627a49901cd7", "memouser2"))
        self.memorepo = memo_repository
        self.before = self.memorepo.count()
        self.memo = get_test_memo()
        self.saved_memo = self.memorepo.new(self.memo)

    def tearDown(self):
        self.userrepo.remove(self.user)
        self.userrepo.remove(self.user_two)
        disconnect_database()

    # count
    def test_count_defaults_to_all_memos(self):
        for i in range(1, 4):
            self.memorepo.new(get_test_memo())
        count = self.memorepo.count()
        memos = self.memorepo.get()
        self.assertEqual(count, len(memos))

    def test_count_all_memos_works(self):
        before = self.memorepo.count("all")
        self.memorepo.new(get_test_memo())
        after = self.memorepo.count("all")
        self.assertEqual(after, before + 1)

    def test_count_all_with_multiple_added_works(self):
        before = self.memorepo.count()
        for i in range(1, 4):
            memo = get_test_memo(i)
            self.memorepo.new(memo)
        after = self.memorepo.count()
        self.assertEqual(after, before + 3)

    def test_count_id_returns_only_one(self):
        result = self.memorepo.count('id', self.saved_memo.id)
        self.assertEqual(result, 1)

    def test_count_not_valid_id_returns_zero(self):
        result = self.memorepo.count('id', get_id())
        self.assertEqual(result, 0)

    def test_count_author_returns_right_amount(self):
        for i in range(3):
            memo = get_test_memo()
            memo["author"] = self.user_two
            self.memorepo.new(memo)
        result = self.memorepo.count("author", self.user_two)
        self.assertEqual(result, 3)

    # new - ok
    def test_new_memo_returns_created_memo(self):
        self.assertIsNotNone(self.saved_memo.id)
        self.assertEqual(self.saved_memo.author, self.memo["author"])
        self.assertEqual(self.saved_memo.title, self.memo["title"])
        self.assertEqual(self.saved_memo.content, self.memo["content"])
        self.assertEqual(self.saved_memo.date, self.memo["date"])

    def test_new_memo_increases_amount_of_memos(self):
        after = self.memorepo.count()
        self.assertEqual(after, self.before+1)

    # update
    def test_update_memo_updates_values(self):
        self.saved_memo.title = "Updated title"
        self.saved_memo.content = "Updated content"
        updated_memo = self.memorepo.update(self.saved_memo)
        self.assertEqual(self.saved_memo.title, updated_memo.title)
        self.assertEqual(self.saved_memo.content, updated_memo.content)
        self.assertEqual(self.saved_memo.author, updated_memo.author)

    def test_update_memo_updates_values_to_db(self):
        self.saved_memo.title = "Updated title"
        self.saved_memo.content = "Updated content"
        updated_memo = self.memorepo.update(self.saved_memo)
        memo_in_db = self.memorepo.get('id', self.saved_memo.id)
        self.assertEqual(memo_in_db, updated_memo)

    # remove
    def test_remove_memo_removes_from_database(self):
        result = self.memorepo.remove(self.saved_memo)
        self.assertEqual(self.memorepo.count(), self.before)
        self.assertTrue(result)

    def test_remove_memo_returns_false_if_not_valid_memo(self):
        not_valid_memo = get_test_memo_obj()
        result = self.memorepo.remove(not_valid_memo)
        self.assertFalse(result)

    def test_remove_memo_with_none_memo_returns_false(self):
        result = self.memorepo.remove(None)
        self.assertFalse(result)

    # get
    def test_get_defaults_get_all(self):
        for i in range(1, 4):
            self.memorepo.new(get_test_memo(i))
        count = self.memorepo.count()
        memos = self.memorepo.get()
        self.assertEqual(len(memos), count)

    def test_get_all_returns_list_of_memos(self):
        added_memos = []
        added_memos.append(self.saved_memo)
        for i in range(1, 4):
            added_memos.append(self.memorepo.new(get_test_memo(i)))
        memos = self.memorepo.get("all")
        for i in range(len(memos)):
            self.assertEqual(memos[i], added_memos[i])

    def test_get_id_returns_memo_with_same_id(self):
        queried_memo = self.memorepo.get('id', self.saved_memo.id)
        self.assertEqual(queried_memo, self.saved_memo)
        self.assertEqual(queried_memo.id, self.saved_memo.id)
        self.assertEqual(queried_memo.title, self.saved_memo.title)
        self.assertEqual(queried_memo.content, self.saved_memo.content)

    def test_get_unvalid_id(self):
        queried_memo = self.memorepo.get('id', get_id())
        self.assertIsNone(queried_memo)

    def test_get_author_id_with_author_works(self):
        user_two_memo = get_test_memo()
        user_two_memo["author"] = self.user_two
        self.memorepo.new(user_two_memo)
        queried_memos = self.memorepo.get(
            "author", self.saved_memo.author)
        self.assertEqual(len(queried_memos), 1)
        queried_memo = queried_memos[0]
        self.assertEqual(queried_memo.id, self.saved_memo.id)
        self.assertEqual(queried_memo.author, self.saved_memo.author)
