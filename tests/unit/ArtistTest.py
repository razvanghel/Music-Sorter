import unittest

from model.artists.Artist import Artist
from tests.frameworks.Generator import Generator

expected = Generator.random_artist()

class ArtistTest(unittest.TestCase):

    def setUp(self):
        self.artist = Artist("", "")
        self.artist.set_name(expected.get_name())
        self.artist.set_path(expected.get_path())

    def test_name(self):
        self.assertEqual(expected.get_name(), self.artist.get_name())
        e = "test"
        self.artist.set_name(e)
        self.assertEqual(e, self.artist.get_name())


    def test_path(self):
        self.assertEqual(expected.get_path(), self.artist.get_path())
        e = "test"
        self.artist.set_path(e)
        self.assertEqual(e, self.artist.get_path())