import unittest
import random

from tinytag import TinyTag

from model.artists.Artists import Artists
from model.top_buttons.ActionCreate import ActionCreate, ActionType, ActionMove
from model.top_buttons.AddUndo import AddUndo
from tests import TestHelper as t
from tests.frameworks.Generator import Generator as g
from handlers import FileHandler as f

class AddUndoTest(unittest.TestCase):

    def setUp(self):
        t.setUp()
        self.artists = g.random_generated_artists()
        self.add = AddUndo()

    def test_undo(self):
        artists = g.random_generated_artists()
        songs = g.random_songs_of_artists(artists.get_all_artists())
        for song in songs:
            self.assertTrue(f.is_file(song.get_path()))
        add = self.add
        self.assertTrue(add.get_history().is_empty())
        add.add_songs(songs, artists)
        self.assertFalse(add.get_history().is_empty())
        for song in songs:
            self.assertFalse(f.is_file(song.get_path()))

        for action in add.get_history().get_last_action_array():
            path = action.get_current_path()
            self.assertTrue(f.exists(path))

        add.undo()
        self.assertTrue(add.get_history().is_empty())
        for song in songs:
            self.assertTrue(f.is_file(song.get_path()))

    def test_get_history(self):
        add = self.add
        self.assertTrue(add.get_history().is_empty())
        h = g.random_history()
        add.set_history(h)
        self.assertEqual(h, add.get_history())

    def test_add_song(self):
        song = g.random_generated_song()
        a = TinyTag.get(song.get_path())
        artist = self._random_artist()
        new_path = artist.get_path()+f"\\{song.get_name()}"
        self.assertFalse(f.is_file(new_path))
        self.assertTrue(f.is_file(song.get_path()))
        action = ActionMove(song.get_path(), new_path)
        self.add._add_song(song, artist)
        self.assertTrue(f.is_file(new_path))

        h = self.add.get_history()
        self._check_action(action, h.get_last_action_array())

    def _check_action(self, expected, actual):
        self.assertEqual(expected.get_type(), actual.get_type())
        self.assertEqual(expected.get_current_path(), actual.get_current_path())
        if expected.get_type() == ActionType.MOVE:
            self.assertEqual(expected.get_old_path(), actual.get_old_path())

    def _random_artist(self):
        list = self.artists.get_all_artists()
        return list[random.randint(0,len(list)-1)]

    def test_add_songs(self):
        songs = g.random_generated_song_list()
        artist = g.random_generated_artist()
        list = []
        for song in songs:
            list.append(ActionMove(song.get_path(), f.combine_paths(artist.get_path(), song.get_name())))

        self.add.add_songs(songs, artist)
        # self._check_action_lists(list, self.add.get_history().get_array())

    def test_auto_add_new_artists(self):
        new_artists = g.random_artists().get_all_artists()
        new_added_songs = g.random_songs_of_artists(new_artists)
        path = t.genres_path
        self.add.auto_add(Artists(path), songs=new_added_songs,
                          path=path)

        actual = self.add.new_added_artists
        self._check_list(new_artists, actual)

    def test_auto_add(self):
        new_artists = g.random_artists().get_all_artists()
        new_added_songs = g.random_songs_of_artists(new_artists)
        artist = g.random_generated_artist()
        song = g.random_generated_song_of_known_artist(artist)
        songs = new_added_songs
        songs.append(song)
        path = t.genres_path
        a = Artists(path)
        a.add_artist(artist)
        self.add.auto_add(a, songs=songs,
                          path=path)

        actual = self.add.new_added_artists
        self._check_list(new_artists, actual)

    def test_auto_add_unsorted_songs(self):
        expected_unsorted_songs = g.random_generated_song_list()
        self.add.auto_add(Artists(t.genres_path), songs= expected_unsorted_songs,
                          path=t.genres_path)
        self._check_songs(expected_unsorted_songs, self.add.unsorted_songs_list)

    def _check_songs(self, e_list, a_list):
        self.assertEqual(len(e_list), len(a_list))
        for e in range(0, len(e_list) - 1):
            expected = e_list[e]
            actual = a_list[e]
            self.assertEqual(expected.get_name(), actual.get_name())
            self.assertEqual(expected.get_album_artist(), actual.get_album_artist())
            self.assertEqual(expected.get_artist(), actual.get_artist())
            self.assertEqual(expected.get_path(), actual.get_path())
            self.assertEqual(expected.get_title(), actual.get_title())
            try:
                self.assertEqual(expected.get_genre(), actual.get_genre()())
            except:
                self.assertIsNone(expected.get_genre())
                self.assertIsNone(actual.get_genre())

    """
    Appends the second list to the first list
    """
    def _combine_lists(self, l1, l2):
        return l1 + l2

    def tearDown(self):
        t.tearDown()

    def _create_expected_history(self, songs):
        pass

    def _check_action_lists(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for i in range(0, len(expected) - 1):
            self._check_action(expected[i], actual[i])

    def _check_list(self, expected_list, actual_list):
        self.assertEqual(len(expected_list), len(actual_list))
        for e in range(0, len(expected_list) - 1):
            expected = expected_list[e]
            actual = actual_list[e]
            self.assertEqual(expected.get_name(), actual.get_name())

    def _artist_found(self, name, all_artists):
        return all_artists.get_artist_by_name(name) != None