import unittest
from datetime import datetime
from freezegun import freeze_time
from bson.objectid import ObjectId
from entities.memo import Memo


@freeze_time(datetime.utcnow())
class TestMemo(unittest.TestCase):
    def setUp(self):
        self.author_id = ObjectId("605f5d100f27ca5baf32b16b")
        self.title = "Test Memo"
        self.content = "Lorem ipsum dolor sit amet."
        self.date = datetime.utcnow()
        self.memo = Memo(self.author_id, self.title, self.content)

    def test_memo_initializes_with_title_and_content(self):
        self.assertEqual(self.memo.author_id, self.author_id)
        self.assertEqual(self.memo.title, self.title)
        self.assertEqual(self.memo.content, self.content)
        self.assertEqual(self.memo.date, self.date)
        self.assertIsNotNone(self.memo.id)

    def test_memo_initializes_without_title_and_content(self):
        # initialize memo
        self.memo = Memo(self.author_id)

        # test
        self.assertEqual(self.memo.author_id, self.author_id)
        self.assertEqual(self.memo.title, "Memo " +
                         str(datetime.utcnow().isoformat()))
        self.assertEqual(self.memo.content, "")
        self.assertEqual(self.memo.date, self.date)
        self.assertIsNotNone(self.memo.id)

    def test_memo_function_format_works(self):
        self.memo = Memo(self.author_id, self.title, self.content,
                         ObjectId("605f5c9b9f6075e6c82c104b"))
        memo_dict = {
            "id": ObjectId("605f5c9b9f6075e6c82c104b"),
            "title": self.title,
            "content": self.content,
            "author_id": ObjectId("605f5d100f27ca5baf32b16b"),
            "date": self.date,
        }
        self.assertEqual(self.memo.format(), memo_dict)
