import unittest
from freezegun import freeze_time
from utils.helpers import get_time, get_test_memo, get_id
from repositories.MemoRepository import MemoRepository


@freeze_time(get_time())
class TestMemoRepository(unittest.TestCase):

    def setUp(self):
        self.memorepo = MemoRepository(prod=False)
        self.before = self.memorepo.count('all')
        self.memo = get_test_memo()
        self.saved_memo = self.memorepo.new(self.memo)

    def test_count_memos_works(self):
        before = self.memorepo.count('all')
        self.memorepo.new_memo(get_test_memo())
        after = self.memorepo.count('all')
        self.assertEqual(after, before + 1)

    def test_get_all_memos_returns_memos(self):
        for i in range(1, 4):
            memo = get_test_memo(i)
            self.memorepo.new(memo)
        after = self.memorepo.count('all')
        self.assertEqual(after, self.before + 3)

    def test_get_id_returns_memo_with_same_id(self):
        queried_memo = self.memorepo.get('id', self.saved_memo.id)
        self.assertEqual(self.saved_memo.id, queried_memo.id)
        self.assertEqual(self.saved_memo.title, queried_memo.title)
        self.assertEqual(self.saved_memo.content, queried_memo.content)
        self.assertEqual(self.saved_memo.author_id, queried_memo.author_id)

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

    def test_get_author_id_with_author_id_works(self):
        filtered_memos = self.memorepo.get(
            "author_id", self.saved_memo.author_id)
        self.assertEqual(filtered_memos.count(), 1)
        filtered_memo = filtered_memos.first()
        self.assertEqual(filtered_memo.id, self.saved_memo.id)
        self.assertEqual(filtered_memo.author_id, self.saved_memo.author_id)

    def test_new_memo_returns_created_memo(self):
        self.assertIsNotNone(self.saved_memo.id)

    def test_new_memo_increases_amount_of_memos(self):
        after = self.memorepo.count('all')
        self.assertEqual(after, self.before+1)

    def test_update_memo_updates_values(self):
        memo = self.memorepo.new(get_test_memo())
        memo.title = "Updated title"
        memo.content = "Updated content"
        updated_memo = self.memorepo.update(memo)
        self.assertEqual(memo.title, updated_memo.title)
        self.assertEqual(memo.content, updated_memo.content)
        self.assertEqual(memo.author_id, updated_memo.author_id)

    def test_remove_memo_removes_from_database(self):
        memo_to_be_removed = self.memorepo.new(get_test_memo())
        removed_memo = self.memorepo.remove(memo_to_be_removed.id)
        self.assertEqual(self.memorepo.count('all'), self.before)
        self.assertTrue(removed_memo)

    def test_remove_memo_returns_false_if_not_valid_id(self):
        unvalid_id = get_id()
        removed_memo = self.memorepo.remove(unvalid_id)
        self.assertFalse(removed_memo)
