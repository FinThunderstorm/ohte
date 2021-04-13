import unittest
from freezegun import freeze_time
from entities.memo import Memo

from utils.helpers import get_time, get_test_memo


@freeze_time(get_time())
class TestMemo(unittest.TestCase):
    def setUp(self):
        self.memo = get_test_memo()
        self.new_memo = Memo(author=self.memo["author"], title=self.memo["title"],
                             content=self.memo["content"], date=self.memo["date"])

    def test_memo_initializes_with_title_and_content(self):
        self.assertEqual(self.new_memo.author, self.memo["author"])
        self.assertEqual(self.new_memo.title, self.memo["title"])
        self.assertEqual(self.new_memo.content, self.memo["content"])
        self.assertEqual(self.new_memo.date, self.memo["date"])
