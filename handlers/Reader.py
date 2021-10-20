import os
from enum import Enum

from model.artists.Artist import Artist
from model.genre.Genre import Genre
from model.song.SongGUI import SongGUI
from handlers import FileHandler as f
from model.sounds.library_sound import LibrarySound


class SongType(Enum):
    FLAC = ".flac"
    WAV = ".wav"
    MP3 = ".mp3"
    AIFF = ".aiff"
    AIF = ".aif"

    @staticmethod
    def values():
        list = []
        list.append(SongType.FLAC)
        list.append(SongType.WAV)
        list.append(SongType.MP3)
        list.append(SongType.AIFF)
        list.append(SongType.AIF)
        return list

    def toString(self):
        return self.value




ACCEPTED_FORMATS = SongType.values()
class Reader:

    @staticmethod
    def is_accepted(data):
        for type in ACCEPTED_FORMATS:
             if str(data).lower().endswith(type.toString()):
                return type
        return None

    @staticmethod
    def _read_wav(root, data, width):
        song = SongGUI(root, data, width)
        return song

    @staticmethod
    def read_sounds_from_library(path, previous = ""):
        list = []
        if len(Reader._filter_sounds(path)) == 0:
            return []

        for dir in Reader._filter_sounds(path):
            list += Reader.read_sounds_from_library(dir, f.extract_from_path(dir))
            list.append(LibrarySound(dir, f.extract_from_path(dir), previous))

        return list

    @staticmethod
    def read_songs(root, data, width):
        arrays = Reader.format_data(data)
        songs = []
        for element in arrays:
            song = Reader.read_song(root,element, width)
            songs.append(song)
        return songs

    @staticmethod
    def read_song(root, data, width):
        type = Reader.is_accepted(data)
        if type != None:
            return Reader._read_wav(root, data, width)
        else:
            raise TypeError(f"File format not accepted. Accepted formats: ACCEPTED_FORMATS")

    @staticmethod
    def format_data(data):
        arrays = data.split("}")
        for i in range(0, len(arrays) - 1):
            arr = arrays[i].split("{")
            arrays[i] = arr[1]
        return arrays[:-1]

    @staticmethod
    def get_children_of_folder(root):
        dirlist = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]

        return dirlist

    @staticmethod
    def get_children_as_paths(path):
        dirlist = [os.path.join(path, item) for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]
        return dirlist

    @staticmethod
    def read_artists(path):
        content = Reader.get_children_of_folder(path)
        genres = {}
        for name in content:
            genre = Genre(path, name)
            artists = []
            for artistName in Reader.get_children_of_folder(genre.get_path()):
                artist = Artist(genre, artistName)
                artists.append(artist)
            genres[genre] = artists

        return genres

    @classmethod
    def _filter_sounds(cls, path):
        result = [child for child in Reader.get_children_as_paths(path) if f.is_dir(child)]
        return result
