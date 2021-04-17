import unittest
from freezegun import freeze_time
from utils.helpers import get_time, get_test_memo, get_test_memo_user, get_id, get_test_memo_obj
from utils.database_handler import connect_database, disconnect_database
from repositories.MemoRepository import memo_repository
from repositories.UserRepository import user_repository


@freeze_time(get_time())
class TestMemoRepository(unittest.TestCase):

    def setUp(self):
        connect_database(prod=False)
        self.userrepo = user_repository
        self.user = self.userrepo.update(get_test_memo_user())
        user_two = get_test_memo_user("6072d33e3a3c627a49901cd7", "memouser2")
        self.user_two = self.userrepo.update(user_two)
        self.memorepo = memo_repository
        self.before = self.memorepo.count()
        self.memo = get_test_memo()
        self.saved_memo = self.memorepo.new(self.memo)
        print('Is there our user?', self.userrepo.get('id', self.user.id))

    def tearDown(self):
        self.userrepo.remove(self.user)
        self.userrepo.remove(self.user_two)
        disconnect_database()

    # count
    def test_count_memos_works(self):
        before = self.memorepo.count()
        self.memorepo.new(get_test_memo())
        after = self.memorepo.count()
        self.assertEqual(after, before + 1)

    def test_count_with_multiple_added_works(self):
        before = self.memorepo.count()
        for i in range(1, 4):
            memo = get_test_memo(i)
            self.memorepo.new(memo)
        after = self.memorepo.count()
        self.assertEqual(after, before + 3)

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

    # get
    def test_get_defaults_get_all(self):
        for i in range(1, 4):
            self.memorepo.new(get_test_memo(i))
        count = self.memorepo.count()
        memos = self.memorepo.get()
        self.assertEqual(len(memos), count)

    def test_get_all_returns_list_of_memos(self):
        added_memos = []
        for i in range(1, 4):
            added_memos.append(self.memorepo.new(get_test_memo(i)))
        memos = self.memorepo.get("all")
        for i in range(1, 4):
            self.assertEqual(memos[i], added_memos[i-1])

    def test_get_id_returns_memo_with_same_id(self):
        queried_memo = self.memorepo.get('id', self.saved_memo.id)
        self.assertEqual(self.saved_memo, queried_memo)
        self.assertEqual(self.saved_memo.id, queried_memo.id)
        self.assertEqual(self.saved_memo.title, queried_memo.title)
        self.assertEqual(self.saved_memo.content, queried_memo.content)

    def test_get_title_with_title_works(self):
        self.memo["title"] = "Filtered memo"
        saved_test_memo = self.memorepo.new(self.memo)
        filtered_memos = self.memorepo.get("title", "filtered")
        self.assertEqual(filtered_memos.count(), 1)
        filtered_memo = filtered_memos.first()
        self.assertEqual(filtered_memo.id, saved_test_memo.id)
        self.assertEqual(filtered_memo.title, saved_test_memo.title)

    def test_get_content_with_content_works(self):
        self.memo["content"] = "Lorem ipsum FiLtErEd dolor sit amet."
        saved_test_memo = self.memorepo.new(self.memo)
        filtered_memos = self.memorepo.get("content", "filtered")
        self.assertEqual(filtered_memos.count(), 1)
        filtered_memo = filtered_memos.first()
        self.assertEqual(filtered_memo.id, saved_test_memo.id)
        self.assertEqual(filtered_memo.content, saved_test_memo.content)

    def test_get_author_id_with_author_works(self):
        user_two_memo = get_test_memo()
        user_two_memo["author"] = self.user_two
        self.memorepo.new(user_two_memo)
        filtered_memos = self.memorepo.get(
            "author", self.saved_memo.author)
        self.assertEqual(len(filtered_memos), 1)
        filtered_memo = filtered_memos[0]
        self.assertEqual(filtered_memo.id, self.saved_memo.id)
        self.assertEqual(filtered_memo.author, self.saved_memo.author)
