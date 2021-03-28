import unittest
from freezegun import freeze_time
from utils.helpers import get_time, get_test_memo, get_id
from repositories.MemoRepository import MemoRepository


@freeze_time(get_time())
class TestMemoRepository(unittest.TestCase):

    def setUp(self):
        self.memorepo = MemoRepository(prod=False)

    def test_count_memos_works(self):
        self.assertEqual(self.memorepo.count_memos(), 0)
        self.memorepo.new_memo(get_test_memo())
        self.assertEqual(self.memorepo.count_memos(), 1)

    def test_get_all_memos_returns_memos(self):
        before = self.memorepo.count_memos()
        for i in range(1, 4):
            memo = get_test_memo(i)
            self.memorepo.new_memo(memo)
        all_memos = self.memorepo.get_all_memos()
        self.assertEqual(len(all_memos), before + 3)

    def test_get_memo_returns_memo_with_same_id(self):
        memo = get_test_memo()
        saved_memo = self.memorepo.new_memo(memo)
        queried_memo = self.memorepo.get_memo(saved_memo.id)
        self.assertEqual(saved_memo.id, queried_memo.id)
        self.assertEqual(saved_memo.title, queried_memo.title)
        self.assertEqual(saved_memo.content, queried_memo.content)
        self.assertEqual(saved_memo.author_id, queried_memo.author_id)

    def test_new_memo_returns_created_memo(self):
        memo = get_test_memo()
        new_memo = self.memorepo.new_memo(memo)
        self.assertIsNotNone(new_memo.id)

    def test_new_memo_increases_amount_of_memos(self):
        before = self.memorepo.count_memos()
        memo = get_test_memo()
        self.memorepo.new_memo(memo)
        self.assertEqual(self.memorepo.count_memos(), before+1)

    def test_update_memo_updates_values(self):
        memo = self.memorepo.new_memo(get_test_memo())
        memo.title = "Updated title"
        memo.content = "Updated content"
        updated_memo = self.memorepo.update_memo(memo)
        self.assertEqual(memo.title, updated_memo.title)
        self.assertEqual(memo.content, updated_memo.content)
        self.assertEqual(memo.author_id, updated_memo.author_id)

    def test_remove_memo_removes_from_database(self):
        before = self.memorepo.count_memos()
        memo_to_be_removed = self.memorepo.new_memo(get_test_memo())
        removed_memo = self.memorepo.remove_memo(memo_to_be_removed.id)
        self.assertEqual(self.memorepo.count_memos(), before)
        self.assertTrue(removed_memo)

    def test_remove_memo_returns_false_if_not_valid_id(self):
        unvalid_id = get_id()
        removed_memo = self.memorepo.remove_memo(unvalid_id)
        self.assertFalse(removed_memo)

    def test_filter_memos_with_title_works(self):
        test_memo = get_test_memo()
        test_memo["title"] = "Filtered memo"
        saved_test_memo = self.memorepo.new_memo(test_memo)
        filtered_memos = self.memorepo.filter_memos("title", "filtered")
        self.assertEqual(filtered_memos.count(), 1)
        filtered_memo = filtered_memos.first()
        self.assertEqual(filtered_memo.id, saved_test_memo.id)
        self.assertEqual(filtered_memo.title, saved_test_memo.title)

    def test_filter_memos_with_content_works(self):
        test_memo = get_test_memo()
        test_memo["content"] = "Lorem ipsum FiLtErEd dolor sit amet."
        saved_test_memo = self.memorepo.new_memo(test_memo)
        filtered_memos = self.memorepo.filter_memos("content", "filtered")
        self.assertEqual(filtered_memos.count(), 1)
        filtered_memo = filtered_memos.first()
        self.assertEqual(filtered_memo.id, saved_test_memo.id)
        self.assertEqual(filtered_memo.content, saved_test_memo.content)

    def test_filter_memos_with_author_id(self):
        saved_test_memo = self.memorepo.new_memo(get_test_memo())
        filtered_memos = self.memorepo.filter_memos(
            "author_id", saved_test_memo.author_id)
        self.assertEqual(filtered_memos.count(), 1)
        filtered_memo = filtered_memos.first()
        self.assertEqual(filtered_memo.id, saved_test_memo.id)
        self.assertEqual(filtered_memo.author_id, saved_test_memo.author_id)
