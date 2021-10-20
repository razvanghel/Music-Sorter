import unittest
import random

from model.artists.Artists import Artists
from tests.frameworks.Generator import Generator
from tests.TestHelper import genres_path
path = genres_path

class ArtistsTest(unittest.TestCase):

    def setUp(self):
        expected = Generator.random_artists_dict()
        self.a = Artists(path, expected)
        self.expected_dict = expected

    def test_get_dict(self):
        expected = self.expected_dict
        dict = self.a.get_dict()
        self.assertEqual(len(expected.keys()), len(dict))
        for key in expected.keys():
            self.assertTrue(key in dict)
            array = expected[key]
            self.assertEqual(len(array), len(dict[key]))
            for e_artist in array:
                self.assertTrue(e_artist in dict[key])

    def test_get_artist_names(self):
        expected = self.expected_dict
        a = self.a
        for name in a.get_artist_names():
            self.assertTrue(self._is_in_dict(expected, name))


    def test_get_genres(self):
        expected = self.expected_dict
        a = self.a
        self.assertEqual(expected.keys(), a.get_genres())

    def test_get_path(self):
        a = self.a
        self.assertEqual(path,a.get_path())

    def test_get_artist_by_name(self):
        expected = Generator.random_artists_dict()
        a = Artists(path, expected)
        for key in expected.keys():
            artists = expected[key]
            actual_list = a.get_dict()
            self.assertEqual(len(artists), len(actual_list[key]))
            for artist in artists:
                self._check_artist(artist, a.get_artist_by_name(artist.get_name()))

    def test_get_artist_of_genre(self):
        expected = self.expected_dict
        a = self.a
        r = random.randint(0, len(expected.keys())-1)
        random_genre = list(expected.keys())[r]
        random_artists = expected[random_genre]
        actual = a.get_artists_of_genre(random_genre)
        for artist in random_artists:
            self.assertTrue(artist in actual)

    def test_get_all_artists(self):
        dict = self.expected_dict
        expected = []
        for k in dict.keys():
            arr = dict[k]
            for a in arr:
                expected.append(a)

        for expected_artist in expected:
            self.assertTrue(expected_artist in self.a.get_all_artists())

    def _check_artist(self, expected, actual):
        self.assertEqual(expected.get_name(), actual.get_name())
        self.assertEqual(expected.get_path(), actual.get_path())

    def _is_in_dict(self, expected, name):
        for key in expected.keys():
            array = expected[key]
            expect = []
            for artist in array:
                expect.append(artist.get_name())
            if name in expect:
                return True

        return False