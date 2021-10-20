import tkinter

from tinytag import TinyTag
from handlers import PathCreator
from handlers import FileHandler as f
from model.sounds.sound import Sound


class Song(Sound):

    def __init__(self, path = None, file_name = None, artist = None, title = None, album_artist = None, genre = None):
        super().__init__(path, file_name)
        self._artist = artist
        self._title = title
        self._album_artist = album_artist
        self.genre = genre

    def get_artist(self):
        return self._artist

    def get_genre(self):
        return self.genre

    def get_title(self):
        return self._title

    def get_album_artist(self):
        return self._album_artist

    def set_album_artist(self, album_artist):
        self._album_artist = album_artist

    def set_artist(self, artist):
        self._artist = artist

    def set_title(self, title):
        self._title = title

    def __eq__(self, other):
        if self._path != other.get_path():
            return False
        elif self._artist != other.get_artist():
            return False
        elif self._title != other.get_title():
            return False
        elif self._album_artist != other.get_album_artist():
            return False
        elif self._file_name != other.get_name():
            return False
        return True

    def __lt__(self, other):
        return self.name < other

    def __gt__(self, other):
        return self.name > other

    def change_name(self, name):
        self._path.replace(self.get_name(), name)
        self.set_name(name)

