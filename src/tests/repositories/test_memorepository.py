import unittest
from freezegun import freeze_time
from utils.helpers import get_time, get_test_memo
from repositories.MemoRepository import MemoRepository


@freeze_time(get_time())
class TestMemoRepository(unittest.TestCase):

    def setUp(self):
        self.memorepo = MemoRepository(prod=False)

    def test_get_all_memos_returns_memos(self):
        for i in range(1, 4):
            memo = get_test_memo(i)
            self.memorepo.new_memo(memo)
        all_memos = self.memorepo.get_all_memos()
        self.assertEqual(len(all_memos), 3)

    def test_new_memo_returns_created_memo(self):
        memo = get_test_memo()
        new_memo = self.memorepo.new_memo(memo)
        self.assertIsNotNone(new_memo.id)

    def test_new_memo_increases_amount_of_memos(self):
        before = self.memorepo.count_memos()
        memo = get_test_memo()
        new_memo = self.memorepo.new_memo(memo)
        self.assertEqual(self.memorepo.count_memos(), before+1)
