import unittest
from freezegun import freeze_time
from utils.helpers import get_time, get_test_memo, get_test_memo_user, get_id
from utils.database_handler import connect_database, disconnect_database
from repositories.MemoRepository import memo_repository
from repositories.UserRepository import user_repository


@freeze_time(get_time())
class TestMemoRepository(unittest.TestCase):

    def setUp(self):
        connect_database(prod=False)
        self.memorepo = memo_repository
        self.user = user_repository.new(get_test_memo_user())
        self.before = self.memorepo.count()
        self.memo = get_test_memo()
        self.saved_memo = self.memorepo.new(self.memo)

    def tearDown(self):
        user_repository.remove(self.user)
        disconnect_database()

    def test_count_memos_works(self):
        before = self.memorepo.count()
        self.memorepo.new(get_test_memo())
        after = self.memorepo.count()
        self.assertEqual(after, before + 1)

    def test_get_all_memos_returns_memos(self):
        before = self.memorepo.count()
        for i in range(1, 4):
            memo = get_test_memo(i)
            self.memorepo.new(memo)
        after = self.memorepo.count()
        self.assertEqual(after, before + 3)

    def test_get_id_returns_memo_with_same_id(self):
        queried_memo = self.memorepo.get('id', self.saved_memo.id)
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

    # def test_get_author_id_with_author_works(self):
    #     filtered_memos = self.memorepo.get(
    #         "author", self.saved_memo.author)
    #     self.assertEqual(filtered_memos.count(), 1)
    #     filtered_memo = filtered_memos.first()
    #     self.assertEqual(filtered_memo.id, self.saved_memo.id)
    #     self.assertEqual(filtered_memo.author, self.saved_memo.author)

    def test_new_memo_returns_created_memo(self):
        self.assertIsNotNone(self.saved_memo.id)

    def test_new_memo_increases_amount_of_memos(self):
        after = self.memorepo.count()
        self.assertEqual(after, self.before+1)

    def test_update_memo_updates_values(self):
        self.saved_memo.title = "Updated title"
        self.saved_memo.content = "Updated content"
        updated_memo = self.memorepo.update(self.saved_memo)
        self.assertEqual(self.saved_memo.title, updated_memo.title)
        self.assertEqual(self.saved_memo.content, updated_memo.content)
        self.assertEqual(self.saved_memo.author, updated_memo.author)

    def test_remove_memo_removes_from_database(self):
        removed_memo = self.memorepo.remove(self.saved_memo)
        self.assertEqual(self.memorepo.count(), self.before)
        self.assertTrue(removed_memo)

    def test_remove_memo_returns_false_if_not_valid_memo(self):
        pass
