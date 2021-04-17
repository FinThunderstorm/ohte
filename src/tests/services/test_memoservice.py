import unittest
from freezegun import freeze_time
from utils.database_handler import connect_test_database, disconnect_database
from utils.helpers import get_time, get_time_timestamp, get_test_memo, get_id, get_test_memo_user, get_test_user_obj
from services.memo_service import memo_service
from repositories.UserRepository import user_repository


@freeze_time(get_time())
class TestMemoService(unittest.TestCase):
    def setUp(self):
        connect_test_database()
        self.userrepo = user_repository
        self.author = self.userrepo.update(get_test_memo_user())
        self.second_author = self.userrepo.update(
            get_test_memo_user('6072d33e3a3c627a49901cd7', "memouser2"))
        self.memo_service = memo_service
        self.before = self.memo_service.count()
        self.test_memo = get_test_memo()
        self.saved_memo = self.memo_service.create(
            self.author.id,
            self.test_memo["title"],
            self.test_memo["content"]
        )

    def tearDown(self):
        user_repository.remove(self.author)
        disconnect_database()

    # create
    def test_create_returns_new_memo_with_all_attributes(self):
        title = "Cool new memo"
        content = "This is a test."

        new_memo = self.memo_service.create(self.author.id, title, content)
        self.assertEqual(new_memo.author.id, self.author.id)
        self.assertEqual(new_memo.title, title)
        self.assertEqual(new_memo.content, content)

    def test_create_adds_memo_id_to_user_field(self):
        author = self.userrepo.get('id', self.author.id)
        count = self.memo_service.count('author', self.author.id)
        self.assertEqual(len(author.memos), count)

    def test_create_returns_memo_with_default_title(self):
        new_memo = self.memo_service.create(self.author.id)
        self.assertEqual(new_memo.author.id, self.author.id)
        self.assertEqual(new_memo.title, "Memo " + str(get_time()))
        self.assertEqual(new_memo.content, "")

    def test_create_returns_none_if_not_valid_author(self):
        saved_memo = self.memo_service.create(
            get_test_user_obj("6072d33e3a3c627a49901ce8", "notvalid"),
            "Not valid title",
            "Not valid content",
        )
        self.assertIsNone(saved_memo)

    # update
    def test_update_changes_values(self):
        title = "Updated title"
        content = "My new cool content."
        updated_memo = self.memo_service.update(
            self.saved_memo.id,
            self.saved_memo.author.id,
            title,
            content,
            self.saved_memo.date)
        self.assertIsNotNone(updated_memo)
        self.assertEqual(updated_memo.title, title)
        self.assertEqual(updated_memo.content, content)
        self.assertEqual(updated_memo.id, self.saved_memo.id)
        self.assertEqual(updated_memo.author, self.saved_memo.author)

    def test_update_can_change_date(self):
        other_date = get_time_timestamp(2012, 10, 12, 13, 14, 48)
        updated_memo = self.memo_service.update(
            self.saved_memo.id,
            self.saved_memo.author.id,
            self.saved_memo.title,
            self.saved_memo.content,
            other_date,
        )
        self.assertIsNotNone(updated_memo)
        self.assertEqual(updated_memo.date, other_date)
        self.assertEqual(updated_memo.id, self.saved_memo.id)
        self.assertEqual(updated_memo.author, self.saved_memo.author)

    # remove
    def test_remove_removes_memo_with_valid_id(self):
        before = self.memo_service.count()
        self.memo_service.create(self.author.id)
        result = self.memo_service.remove(self.saved_memo.id)
        after = self.memo_service.count()
        query = self.memo_service.get("id", self.saved_memo.id)
        self.assertTrue(result)
        self.assertIsNone(query)
        self.assertEqual(after, before)

    def test_remove_return_false_with_unvalid_id(self):
        result = self.memo_service.remove(get_id())
        after = self.memo_service.count()
        self.assertFalse(result)
        self.assertEqual(after, self.before+1)

    def test_removes_memo_from_user(self):
        author = self.userrepo.get("id", self.saved_memo.author.id)
        author_memos_count_before = self.memo_service.count(
            "author", author.id)
        result = self.memo_service.remove(self.saved_memo.id)
        author_memos_count_after = self.memo_service.count("author", author.id)
        author_after = self.userrepo.get("id", author.id)
        self.assertTrue(result)
        self.assertEqual(author_memos_count_before, 1)
        self.assertEqual(author_memos_count_after, 0)
        self.assertNotEqual(author_after.memos, author.memos)

    # get
    def test_get_defaults_to_all(self):
        for i in range(1, 4):
            self.memo_service.create(
                self.author.id, "Test Memo " + str(i), "Testing get defaults to all")
        count = self.memo_service.count()
        memos = self.memo_service.get()
        self.assertEqual(len(memos), count)

    def test_get_all_works(self):
        added_memos = []
        for i in range(1, 4):
            added_memos.append(self.memo_service.create(self.author.id))
        memos = self.memo_service.get()
        for i in range(1, 4):
            self.assertEqual(memos[i], added_memos[i-1])

    def test_get_id_returns_only_one(self):
        queried_memo = self.memo_service.get('id', self.saved_memo.id)
        self.assertEqual(queried_memo, self.saved_memo)
        self.assertEqual(queried_memo.id, self.saved_memo.id)
        self.assertEqual(queried_memo.title, self.saved_memo.title)
        self.assertEqual(queried_memo.content, self.saved_memo.content)

    def test_get_not_valid_id_gives_zero(self):
        queried_memo = self.memo_service.get('id', get_id())
        self.assertIsNone(queried_memo)

    def test_get_title_returns_right_memos(self):
        for i in range(3):
            self.memo_service.create(
                self.author.id, "CountXing " + str(i), "Testing them titles")
        memos = self.memo_service.get("title", "countxing")
        for memo in memos:
            self.assertTrue("countxing".lower() in memo.title.lower())

    def test_get_content_returns_right_amount(self):
        for i in range(3):
            self.memo_service.create(
                self.author.id, "Testings " + str(i), "Testing them countYings")
        memos = self.memo_service.get("content", "countying")
        for memo in memos:
            self.assertTrue("countying".lower() in memo.content.lower())

    def test_get_author_returns_right_amount(self):
        for i in range(3):
            self.memo_service.create(
                self.second_author.id, "Testings " + str(i), "Testing them authors")
        memos = self.memo_service.get("author", self.second_author)
        for memo in memos:
            self.assertEqual(memo.author, self.second_author)

    # count
    def test_count_defaults_to_all(self):
        for _ in range(1, 4):
            self.memo_service.create(self.author.id)
        memos = self.memo_service.get()
        count = self.memo_service.count()
        self.assertEqual(count, len(memos))

    def test_count_all_multiple_works(self):
        before = self.memo_service.count('all')
        for _ in range(0, 3):
            self.memo_service.create(self.author.id)
        after = self.memo_service.count('all')
        self.assertEqual(after, before + 3)

    def test_count_all_works(self):
        before = self.memo_service.count("all")
        self.memo_service.create(self.author.id)
        after = self.memo_service.count("all")
        self.assertEqual(after, before + 1)

    def test_count_id_returns_only_one(self):
        result = self.memo_service.count('id', self.saved_memo.id)
        self.assertEqual(result, 1)

    def test_count_not_valid_id_gives_zero(self):
        result = self.memo_service.count('id', get_id())
        self.assertEqual(result, 0)

    def test_count_title_returns_right_amount(self):
        for i in range(3):
            self.memo_service.create(
                self.author.id, "CountXing " + str(i), "Testing them titles")
        result = self.memo_service.count("title", "countxing")
        self.assertEqual(result, 3)

    def test_count_content_returns_right_amount(self):
        for i in range(3):
            self.memo_service.create(
                self.author.id, "Testings " + str(i), "Testing them countYings")
        result = self.memo_service.count("content", "countying")
        self.assertEqual(result, 3)

    def test_count_author_returns_right_amount(self):
        for i in range(3):
            self.memo_service.create(
                self.second_author.id, "Testings " + str(i), "Testing them authors")
        result = self.memo_service.count("author", self.second_author.id)
        self.assertEqual(result, 3)
