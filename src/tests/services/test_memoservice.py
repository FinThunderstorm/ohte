import unittest
from freezegun import freeze_time
from utils.helpers import get_time, get_test_memo, get_id
from services.memo_service import MemoService


@freeze_time(get_time())
class TestMemoService(unittest.TestCase):
    def setUp(self):
        self.memo_service = MemoService()
        self.before = self.memo_service.count()
        self.test_memo = get_test_memo()
        self.saved_memo = self.memo_service.create(
            self.test_memo["author_id"],
            self.test_memo["title"],
            self.test_memo["content"])

    def test_create_returns_new_memo_with_all_attributes(self):
        author_id = get_id()
        title = "Cool new memo"
        content = "This is a test."
        new_memo = self.memo_service.create_new_memo(author_id, title, content)
        self.assertEqual(new_memo.author_id, author_id)
        self.assertEqual(new_memo.title, title)
        self.assertEqual(new_memo.content, content)

#    def test_create_adds_memo_id_to_user_field(self):

    def test_create_returns_memo_with_default_title(self):
        author_id = get_id()
        new_memo = self.memo_service.create_new_memo()
        self.assertEqual(new_memo.author_id, author_id)
        self.assertEqual(new_memo.title, "Memo "+get_time())
        self.assertEqual(new_memo.content, "")

    def test_update_changes_values(self):
        title = "Updated title"
        content = "My new cool content."
        updated_memo = self.memo_service.update(
            self.saved_memo.id,
            self.saved_memo.author_id,
            title,
            content)
        self.assertEqual(updated_memo.title, title)
        self.assertEqual(updated_memo.content, content)
        self.assertEqual(updated_memo.id, self.saved_memo.id)

    def test_remove_removes_memo_with_valid_id(self):
        result = self.memo_service.remove(self.saved_memo.id)
        after = self.memo_service.count("all")
        query = self.memo_service.find("id", self.saved_memo.id)
        self.assertTrue(result)
        self.assertEqual(len(query), 0)
        self.assertEqual(after, self.before-1)

    def test_remove_return_false_with_unvalid_id(self):
        result = self.memo_service.remove(get_id())
        after = self.memo_service.count("all")
        self.assertFalse(result)
        self.assertEqual(after, self.before)

    def test_get_returns_right_memo(self):
        result = self.memo_service.get(self.saved_memo.id)
        self.assertEqual(result.id, self.saved_memo.id)
        self.assertEqual(result.title, self.saved_memo.title)
        self.assertEqual(result.content, self.saved_memo.content)
        self.assertEqual(result.author_id, self.saved_memo.author_id)
        self.assertEqual(result.date, self.saved_memo.date)

    def test_get_returns_none_if_no_memo(self):
        result = self.memo_service.get(get_id())
        self.assertIsNone(result)

    def test_get_all_returns_all_memos(self):
        result = self.memo_service.get_all()
        length = self
        self.assertEqual(length, self.before)
