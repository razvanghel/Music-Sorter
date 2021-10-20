import unittest

from model.song.Song import Song
from tests.frameworks.Generator import Generator

expected = Generator.random_song()

class SongTest(unittest.TestCase):

    def setUp(self):
        self.song = Song()

    def test_name(self):
        song = self.song
        e = Generator.random_string()
        song.set_name(e)
        a = song.get_name()
        self.assertEqual(e, a)

    def test_artist(self):
        e = Generator.random_artist().get_name()
        self.song.set_artist(e)
        a = self.song.get_artist()
        self.assertEqual(e, a)

    def test_path(self):
        e = Generator.random_string()
        self.song.set_path(e)
        a = self.song.get_path()
        self.assertEqual(e, a)

    def test_title(self):
        e = Generator.random_string()
        self.song.set_title(e)
        a = self.song.get_title()
        self.assertEqual(e, a)

    def test_album_artist(self):
        e = expected.get_album_artist()
        self.song.set_album_artist(e)
        a = self.song.get_album_artist()
        self.assertEqual(e, a)