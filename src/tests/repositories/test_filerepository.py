from os import path, remove
import unittest
from repositories.file_repository import file_repository


class TestFileRepository(unittest.TestCase):
    def setUp(self):
        self.filerepo = file_repository

    def test_open_file_with_valid_path_works(self):
        filesrc = path.join(
            path.dirname(__file__), '..', './testdata', 'test1.md')
        filesrc = path.normpath(filesrc)
        file = self.filerepo.open_file(filesrc)
        self.assertEqual(
            file, '# Testing\n\n- first\n- second\n- third\n\n**bold**\n')

    def test_open_file_bytes_with_valid_path_works(self):
        imgsrc = path.join(
            path.dirname(__file__), '..', './testdata', 'testimage2.jpg')
        imgsrc = path.normpath(imgsrc)
        image = self.filerepo.open_file(imgsrc, byte=True)

        self.assertIsNotNone(image)
        self.assertIsInstance(image, type(b'\xe0'))

    def test_open_file_unvalid_path_returns_none(self):
        file = self.filerepo.open_file('unvalid')
        self.assertIsNone(file)

    def test_open_file_unvalid_path_as_bytes_returns_none(self):
        image = self.filerepo.open_file('unvalid', byte=True)
        self.assertIsNone(image)

    def test_save_file_works(self):
        src = path.join(
            path.dirname(__file__), '..', './testdata', 'testsave1.md')
        src = path.normpath(src)
        content = '# Test\n\nTesting lorem ipsum.'
        self.filerepo.save_file(src, content)

        file = self.filerepo.open_file(src)
        self.assertEqual(file, content)
        remove(src)
