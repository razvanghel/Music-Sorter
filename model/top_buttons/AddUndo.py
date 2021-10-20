from tkinter import Button
import os
import shutil


from handlers.PathCreator import PathCreator
from model.artists.Artist import Artist
from model.genre.Genre import Genre
from model.song.SongGUI import SongGUI
from model.top_buttons.ActionCreate import ActionDelete
from model.top_buttons.History import History, ActionCreate, ActionType, ActionMove
from handlers import FileHandler as f
from settings.settings_program import Settings

artists_path = Settings().get_artists_path()
class AddUndo():

    def __init__(self):
        self.unsorted_songs_list = []
        self.new_added_artists = []
        self.failed_undo = []
        self.history = History()

    def undo(self):
        array = self.history.get_last_action_array()
        result = []
        while len(array) > 0:
            while len(array) != 0:
                action = array[-1]
                try:

                    action.reverse_action()
                    if f.is_file(action.get_current_path()):
                        result.append(SongGUI(action.get_old_path()))

                except:
                    self.failed_undo.append(action)

                array.remove(action)
            self.history.remove_last_action_array()
        return result

    def reset_failed_unde(self):
        self.failed_undo = []

    def get_unsorted_songs(self):
        return self.unsorted_songs_list

    def get_new_added_artists(self):
        return self.new_added_artists

    def _add_create(self, path):
        self.history.add_action(ActionCreate(path))

    def _add_delete(self, path):
        self.history.add_action(ActionDelete(path))

    def _add_move(self, old_path, new_path):
        self.history.add_action(ActionMove(old_path, new_path))

    def add_songs(self, songs, artist):
        for song in songs:
            self._add_song(song, artist)
        self.history.next_index()
            
    def _add_song(self, song, artist):
        path = song.get_path().replace("/", "\\")
        new_path = PathCreator.generatePath(artist.get_path(), path.split("\\")[-1])
        old_path = song.get_path()
        assert f.is_file(song.get_path())
        f.move_file(old_path, new_path)
        self._add_move(old_path, new_path)
        
    def auto_add(self, known_artists, songs, path = artists_path):

        for song in songs:
            artist = self._get_artist_from_song(known_artists, song, path)
            if artist == None:
                self.unsorted_songs_list.append(song)
            else:
                assert f.is_file(song.get_path())
                self._add_song(song, artist)
        self.history.next_index()

    def reset(self):
        self.unsorted_songs_list = []
        self.new_added_artists = []
        self.failed_undo = []

    def get_history(self):
        return self.history

    def set_history(self, history):
        self.history = history

    def _get_artist_from_song(self, artists, song, path):
        artist = artists.get_artist_by_name(song.get_artist())
        if artist != None:
            return artist
        artist = artists.get_artist_by_name(song.get_album_artist())
        if artist != None:
            return artist
        for artist in artists.get_artist_names():
            try:
                s1 =-1
                if song.get_artist() != None:
                    s1 = song.get_artist().lower().find(artist.lower())
                s2 = song.get_name().lower().find(artist.lower())
                if s1 + s2 >= -1:
                    return artists.get_artist_by_name(artist)
            except:
                pass

        new_artist = None
        if song.get_artist() != None:
            new_artist = Artist(Genre(path, "Unknown genre"), song.get_artist())
        elif song.get_album_artist() != None:
            new_artist = Artist(Genre(path, "Unknown genre"), song.get_album_artist())

        try:

            if song.get_genre() != None:
                new_artist.change_genre(Genre(path, song.get_genre()))

            # new artist must be created in genre folder
            try:
                f.create_directory(new_artist.get_genre().get_path())
            except:
                assert f.is_dir(new_artist.get_genre().get_path())
                pass

            try:
                f.create_directory(new_artist.get_path())
                self._add_create(new_artist.get_path())
                self.new_added_artists.append(new_artist)
            except:
                assert f.is_dir(new_artist.get_path())
                pass
            return new_artist
        except:
            pass

        return None

    def _create_artist(self, song):
        pass


        