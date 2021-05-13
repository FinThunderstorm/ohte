from os import path
import unittest
from freezegun import freeze_time
from utils.database_handler import connect_test_database, disconnect_database
from utils.helpers import get_time, get_time_timestamp, get_test_memo, get_id, get_test_memo_user, get_test_user_obj
from services.image_service import image_service
from repositories.user_repository import user_repository


@freeze_time(get_time())
class TestImageService(unittest.TestCase):
    def setUp(self):
        connect_test_database()
        self.userrepo = user_repository
        self.image_service = image_service
        self.author = self.userrepo.update(
            get_test_memo_user('6072d33e3a3c627a49901cd7', "memouser2"))
        self.before = self.image_service.count()

    def tearDown(self):
        disconnect_database()

    def test_create_with_valid_works(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, 'testimage1', imgsrc, 600)
        self.assertEqual(image.name, "testimage1")
        self.assertEqual(image.width, 600)
        self.assertEqual(image.filetype, "png")
        self.assertIsNotNone(image.id)
        self.assertIsInstance(image.image, type(""))
        self.assertEqual(self.image_service.count(), self.before+1)

    def test_create_without_name_works(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage2.jpg')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, '', imgsrc, 600)
        self.assertEqual(image.name, "testimage2")
        self.assertEqual(image.width, 600)
        self.assertEqual(image.filetype, "jpeg")
        self.assertIsNotNone(image.id)
        self.assertIsInstance(image.image, type(""))
        self.assertEqual(self.image_service.count(), self.before+1)

    def test_create_without_valid_author_returns_none(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            get_id('608bd901507fc317f17ab300'), 'testimage1', imgsrc, 600)
        self.assertIsNone(image)
        self.assertEqual(self.image_service.count(), self.before)

    def test_create_unvalid_path_returns_none(self):
        image = self.image_service.create(
            self.author.id, 'testimage1', "imgsrc", 600)
        self.assertIsNone(image)
        self.assertEqual(self.image_service.count(), self.before)

    # convert_image
    def test_convert_returns_string(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage2.jpg')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.convert_image(imgsrc)
        self.assertIsNotNone(image)
        self.assertIsInstance(image, type(""))

    def test_convert_returns_none_if_not_found(self):
        image = self.image_service.convert_image("imgsrc")
        self.assertIsNone(image)

    # update
    def test_update_changes_values(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, 'testimage1', imgsrc, 600)

        updated_image = self.image_service.update(
            image.id, image.author.id, "updatedimage1", image.image, image.filetype, 300)

        self.assertEqual(updated_image.id, image.id)
        self.assertEqual(updated_image.name, "updatedimage1")
        self.assertEqual(updated_image.author, image.author)
        self.assertEqual(updated_image.image, image.image)
        self.assertEqual(updated_image.filetype, image.filetype)
        self.assertEqual(updated_image.width, 300)

    # remove

    def test_remove_removes_valid_image(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, 'testimage1', imgsrc, 600)

        result = self.image_service.remove(image.id)
        self.assertTrue(result)
        self.assertEqual(self.image_service.count(), self.before)

    def test_remove_returns_false_with_unvalid_id(self):
        result = self.image_service.remove(get_id('608bd901507fc317f17ab301'))
        self.assertFalse(result)

    # get
    def test_get_defaults_to_all(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, 'testimage1', imgsrc, 600)
        second_image = self.image_service.create(
            self.author.id, 'testimage2', imgsrc, 600)

        images = self.image_service.get()
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], image)
        self.assertEqual(images[1], second_image)

    def test_get_all_works(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, 'testimage1', imgsrc, 600)
        second_image = self.image_service.create(
            self.author.id, 'testimage2', imgsrc, 600)

        images = self.image_service.get('all')
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], image)
        self.assertEqual(images[1], second_image)

    def test_get_name_returns_images(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, 'testimage1', imgsrc, 600)
        second_image = self.image_service.create(
            self.author.id, 'testimage2', imgsrc, 600)
        third_image = self.image_service.create(
            self.author.id, 'otherimage3', imgsrc, 600)

        images = self.image_service.get('name', "testimage")
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], image)
        self.assertEqual(images[1], second_image)

    def test_get_author_returns_images(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, 'testimage1', imgsrc, 600)
        second_image = self.image_service.create(
            self.author.id, 'testimage2', imgsrc, 600)
        third_image = self.image_service.create(
            get_id('608bd901507fc317f17ab300'), 'otherimage3', imgsrc, 600)

        images = self.image_service.get('author', self.author.id)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], image)
        self.assertEqual(images[1], second_image)

    def test_get_author_returns_none_if_unvalid(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, 'testimage1', imgsrc, 600)

        images = self.image_service.get(
            'author', get_id('608bd901507fc317f17ab300'))
        self.assertIsNone(images)

    def test_get_id_returns_only_one(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, 'testimage1', imgsrc, 600)
        second_image = self.image_service.create(
            self.author.id, 'testimage2', imgsrc, 600)
        third_image = self.image_service.create(
            get_id('608bd901507fc317f17ab300'), 'otherimage3', imgsrc, 600)

        images = self.image_service.get('id', image.id)
        self.assertEqual(images, image)
        self.assertEqual(images.id, image.id)
        self.assertEqual(images.image, image.image)
        self.assertEqual(images.name, image.name)

    def test_get_unvalid_id_returns_none(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, 'testimage1', imgsrc, 600)

        images = self.image_service.get(
            'id', get_id('608bd901507fc317f17ab300'))
        self.assertIsNone(images)

    # count
    def test_count_defaults_to_all(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        for i in range(1, 11):
            self.image_service.create(
                self.author.id, 'testimage'+str(i), imgsrc, 600)
        self.assertEqual(self.image_service.count(), 10)

    def test_count_all_works(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        for i in range(1, 11):
            self.image_service.create(
                self.author.id, 'testimage'+str(i), imgsrc, 600)
        self.assertEqual(self.image_service.count('all'), 10)

    def test_count_author_works(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        for i in range(1, 6):
            self.image_service.create(
                self.author.id, 'testimage'+str(i), imgsrc, 600)
        for i in range(6, 11):
            self.image_service.create(
                get_id('608bd901507fc317f17ab300'), 'testimage'+str(i), imgsrc, 600)
        self.assertEqual(self.image_service.count('author', self.author.id), 5)

    def test_count_name_works(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        for i in range(1, 6):
            self.image_service.create(
                self.author.id, 'testimage'+str(i), imgsrc, 600)
        for i in range(6, 11):
            self.image_service.create(
                self.author.id, 'othercase'+str(i), imgsrc, 600)
        self.assertEqual(self.image_service.count('name', 'testimage'), 5)

    def test_count_unvalid_author_returns_zero(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        for i in range(1, 11):
            self.image_service.create(
                self.author.id, 'testimage'+str(i), imgsrc, 600)
        self.assertEqual(self.image_service.count(
            'author', get_id('608bd901507fc317f17ab300')), 0)

    def test_count_name_without_being_database(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        for i in range(1, 11):
            self.image_service.create(
                self.author.id, 'testimage'+str(i), imgsrc, 600)
        self.assertEqual(self.image_service.count(
            'name', 'othercase'), 0)

    def test_count_valid_id_returns_only_one(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        image = self.image_service.create(
            self.author.id, 'testimage0', imgsrc, 600)
        for i in range(1, 11):
            self.image_service.create(
                self.author.id, 'testimage'+str(i), imgsrc, 600)
        self.assertEqual(self.image_service.count(
            'id', image.id), 1)

    def test_count_unvalid_id_returns_zero(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage1.png')
        imgsrc = path.normpath(imgsrc)
        for i in range(1, 11):
            self.image_service.create(
                self.author.id, 'testimage'+str(i), imgsrc, 600)
        self.assertEqual(self.image_service.count(
            'id', get_id('608bd901507fc317f17ab300')), 0)
