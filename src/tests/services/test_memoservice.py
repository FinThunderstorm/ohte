from os import path, remove
import unittest
from freezegun import freeze_time
from utils.database_handler import connect_test_database, disconnect_database
from utils.helpers import get_time, get_time_timestamp, get_test_memo, get_id, get_test_memo_user, get_test_user_obj
from services.memo_service import memo_service
from services.image_service import image_service
from repositories.file_repository import file_repository
from repositories.user_repository import user_repository


@freeze_time(get_time())
class TestMemoService(unittest.TestCase):
    def setUp(self):
        connect_test_database()
        self.userrepo = user_repository
        self.filerepo = file_repository
        self.author = self.userrepo.update(get_test_memo_user())
        self.second_author = self.userrepo.update(
            get_test_memo_user('6072d33e3a3c627a49901cd7', "memouser2"))
        self.memo_service = memo_service
        self.image_service = image_service
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
        memo_id = self.saved_memo.id
        before = self.memo_service.count()
        result = self.memo_service.remove(memo_id)
        after = self.memo_service.count()
        query = self.memo_service.get("id", memo_id)
        self.assertTrue(result)
        self.assertIsNone(query)
        self.assertEqual(after, before - 1)

    def test_remove_return_false_with_unvalid_id(self):
        before = self.memo_service.count()
        result = self.memo_service.remove(get_id())
        after = self.memo_service.count()
        self.assertFalse(result)
        self.assertEqual(after, before)

    def test_removes_memo_from_user(self):
        self.memo_service.create(self.author.id)
        author = self.userrepo.get("id", self.saved_memo.author.id)
        author_memos_count_before = self.memo_service.count(
            "author", author.id)
        result = self.memo_service.remove(self.saved_memo.id)
        author_memos_count_after = self.memo_service.count("author", author.id)
        author_after = self.userrepo.get("id", author.id)
        self.assertTrue(result)
        self.assertEqual(author_memos_count_before, 2)
        self.assertEqual(author_memos_count_after, 1)
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
        added_memos.append(self.saved_memo)
        for i in range(1, 4):
            added_memos.append(self.memo_service.create(self.author.id))
        memos = self.memo_service.get()
        for i in range(len(memos)):
            self.assertEqual(memos[i], added_memos[i])

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

    def test_import_from_url_returns_valid(self):
        memo = self.memo_service.import_from_url(
            self.author.id, 'https://github.com/FinThunderstorm/ohte/blob/master/src/tests/testdata/test3.md')
        content = "Lorem ipsum dolor sit amet\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce diam mi, pulvinar vitae diam et, faucibus luctus ipsum. Nulla ullamcorper viverra sapien at facilisis. Nullam bibendum cursus metus ac posuere. Nulla faucibus convallis sapien sit amet dapibus. Integer sodales dignissim turpis, id vestibulum tellus euismod ut. Duis vitae velit molestie, interdum purus nec, aliquam sapien. Praesent purus metus, egestas convallis leo nec, faucibus iaculis augue. Nam et mi in nulla tincidunt faucibus.\n\nDonec mauris sapien, hendrerit in mi et, lobortis sodales nulla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec ullamcorper commodo dignissim. Donec aliquet, erat et varius egestas, massa sem fermentum leo, feugiat semper ipsum tellus eget massa. Nulla interdum eu nunc id eleifend. Nam semper mi lorem, ac tristique lectus euismod a. Quisque sagittis sem interdum, varius dolor eget, volutpat arcu. Vestibulum iaculis nec ex vel tristique. Morbi aliquam vulputate vulputate. Vestibulum quis sapien massa. Nulla nec pellentesque ex. Vestibulum cursus purus at justo posuere, sodales maximus tortor auctor.\n\nNunc feugiat vestibulum condimentum. Sed euismod ex vel faucibus bibendum. Pellentesque non orci eget orci bibendum venenatis at id urna. Praesent in felis ante. Pellentesque a euismod diam, at ullamcorper ante. Pellentesque porttitor sagittis nisi vitae tincidunt. Nulla fringilla velit eu sagittis convallis. Duis porttitor quam sed ante faucibus, at imperdiet libero tristique. Nam quis molestie neque.\n\nVestibulum eget urna molestie, ultrices dolor ac, ornare eros. Sed commodo tristique nunc, at vehicula mauris fermentum ac. Morbi sagittis turpis ut consectetur lacinia. In leo lacus, tristique egestas massa nec, ornare molestie massa. Praesent eu velit at velit elementum commodo. Nunc fermentum vehicula mauris a dignissim. Suspendisse fermentum, metus eu egestas ultrices, erat nisi facilisis orci, in lobortis ante dolor mollis libero. Duis tincidunt metus libero, sed ultricies ipsum lacinia a. Nulla nec dictum velit, ut varius mi. In fermentum accumsan sollicitudin. Mauris libero magna, vehicula ac velit eu, laoreet dignissim nulla.\n\nAliquam finibus, leo quis ornare ullamcorper, lectus nibh iaculis nisi, sed rhoncus erat leo sed metus. Praesent quam leo, accumsan at lobortis et, accumsan sit amet augue. Praesent vitae blandit orci, quis scelerisque dolor. Maecenas sed luctus arcu. In a fringilla metus. Etiam a velit ut tortor lacinia vestibulum vel non nisi. Quisque gravida ornare odio. Nunc erat ligula, tristique nec nisl vel, rutrum dignissim elit. Proin eu fermentum lectus. Vestibulum ut imperdiet enim. Nunc semper quam ut nulla auctor, at pharetra massa semper. Aliquam ac mollis libero. Mauris semper, lacus sed tristique accumsan, dolor mi mollis purus, nec gravida enim ex non arcu."
        self.assertEqual(memo.title, 'Imported from github.com')
        self.assertEqual(memo.content, content)
        self.assertEqual(memo.author, self.author)
        self.assertEqual(memo.date, get_time())
        self.assertIsNotNone(memo.id)

    def test_import_from_url_with_unvalid_id_returns_none(self):
        memo = self.memo_service.import_from_url(self.author.id, '')
        self.assertIsNone(memo)

    def test_import_from_file_test_data1_works(self):
        filesrc = path.join(
            path.dirname(__file__), '..', './testdata', 'test1.md')
        filesrc = path.normpath(filesrc)
        content = "# Testing\n\n- first\n- second\n- third\n\n**bold**\n"
        memo = self.memo_service.import_from_file(
            self.author.id, filesrc)
        self.assertIsNotNone(memo)
        self.assertIsNotNone(memo.id)
        self.assertEqual(memo.title, "Imported from test1.md")
        self.assertEqual(memo.content, content)
        self.assertEqual(memo.author, self.author)
        self.assertEqual(memo.date, get_time())

    def test_import_from_file_test_data2_works(self):
        filesrc = path.join(
            path.dirname(__file__), '..', './testdata', 'test2.md')
        filesrc = path.normpath(filesrc)

        memo = self.memo_service.import_from_file(
            self.author.id, filesrc)

        image = self.image_service.get('all')[0]

        content = "| First Column | Second column |\n| ------------ | ------------- |\n| first        | row           |\n| second       | row           |\n\n![](" + \
            str(image.id)+")\n"
        self.assertIsNotNone(memo)
        self.assertIsNotNone(memo.id)
        self.assertEqual(memo.title, "Imported from test2.md")
        self.assertEqual(memo.content, content)
        self.assertEqual(memo.author, self.author)
        self.assertEqual(memo.date, get_time())
        self.assertEqual(self.image_service.count(), 1)

    def test_import_from_file_test_data2_no_duplicate_image_and_uses_only_own_images(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        self.image_service.create(
            self.second_author.id, 'test2.md/testimage1.png', imgsrc, 600)
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage2.jpg')
        imgsrc = path.normpath(imgsrc)
        self.image_service.create(
            self.second_author.id, 'test2.md/testimage1.png', imgsrc, 600)
        filesrc = path.join(
            path.dirname(__file__), '..', './testdata', 'test2.md')
        filesrc = path.normpath(filesrc)
        self.memo_service.import_from_file(
            self.author.id, filesrc)
        second_memo = self.memo_service.import_from_file(
            self.author.id, filesrc)

        image = self.image_service.get('all')
        image = image[2]

        content = "| First Column | Second column |\n| ------------ | ------------- |\n| first        | row           |\n| second       | row           |\n\n![](" + \
            str(image.id)+")\n"
        self.assertIsNotNone(second_memo)
        self.assertIsNotNone(second_memo.id)
        self.assertEqual(second_memo.title, "Imported from test2.md")
        self.assertEqual(second_memo.content, content)
        self.assertEqual(second_memo.author, self.author)
        self.assertEqual(second_memo.date, get_time())
        self.assertEqual(self.image_service.count(), 3)

    def test_import_from_file_unvalid_path_returns_none(self):
        memo = self.memo_service.import_from_file(
            self.author.id, '')
        self.assertIsNone(memo)

    def test_import_from_file_empty_file_returns_none(self):
        filesrc = path.join(
            path.dirname(__file__), '..', './testdata', 'test4.md')
        filesrc = path.normpath(filesrc)
        memo = self.memo_service.import_from_file(
            self.author.id, filesrc)
        self.assertIsNone(memo)

    def test_export_file_makes_file_correctly(self):
        filesrc = path.join(
            path.dirname(__file__), '..', './testdata', 'export1.md')
        filesrc = path.normpath(filesrc)
        self.memo_service.export_memo(self.saved_memo.id, filesrc)
        content = self.filerepo.open_file(filesrc)
        self.assertEqual(content, self.saved_memo.content)
        remove(filesrc)
