import unittest

from model.genre.Genre import Genre
from tests.frameworks.Generator import Generator

expected = Genre(Generator.random_path(), Generator.random_string())

class GenreTest(unittest.TestCase):

    def setUp(self):
        self.g = Genre("", "")
        self.g.setName(expected.get_name())
        self.g.setPath(expected.get_path())

    def test_name(self):
        self.assertEqual(expected.get_name(), self.g.get_name())

    def test_path(self):
        self.assertEqual(expected.get_path(), self.g.get_path())

