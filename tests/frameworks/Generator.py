import os
import random
import shutil

from model.artists.Artist import Artist
from model.artists.Artists import Artists
from model.genre.Genre import Genre
from model.song.Song import Song
from model.top_buttons.ActionCreate import ActionType, ActionCreate, ActionMove
from model.top_buttons.History import History
from tests.TestHelper import genres_path
from tests.TestHelper import songs_path
from tests.TestHelper import dummy_song
from handlers import FileHandler as f
from mutagen.easyid3 import EasyID3
import time

class Generator():

    @staticmethod
    def random_int():
        return random.randint(0, 100)

    @staticmethod
    def random_big_int():
        return random.randint(0, 3000000000)

    @staticmethod
    def random_string():
        random_string = ""
        for _ in range(random.randint(0, 30)):
            random_integer = random.randint(97, 97 + 26 - 1)
            # Keep appending random characters using chr(x)
            random_string += (chr(random_integer))
        if len(random_string) < 2:
            return Generator.random_string()
        return random_string

    @staticmethod
    def random_genre():
        return Genre(genres_path, f"RandomGenre{random.randint(1,15)}")

    @staticmethod
    def random_generated_genre():
        genre = Generator.random_genre()
        try:
            f.create_directory(genre.get_path())
        except:
            pass
        return genre

    @staticmethod
    def random_song(artist = False, album_artist = False, title = False):
        formats = [".mp3"]
        name = f"{Generator.random_string()}"
        file = f"{name}{formats[random.randint(0, len(formats) - 1)]}"
        song = Song(songs_path+f"\\{file}", name, Generator.random_string(), Generator.random_string(), Generator.random_string())
        if not artist:
            song.set_artist(None)
        if not album_artist:
            song.set_album_artist(None)
        if not title:
            song.set_title(None)
        return song


    """ 
    Returns a random song that is also generated in the test folder
    """
    @staticmethod
    def random_generated_song(artist = False, album_artist = False, title = False):
        assert os.path.isdir(songs_path)

        song = Generator.random_song(artist, album_artist , title)
        shutil.copyfile(dummy_song, song.get_path())
        time.sleep(0.5)
        audio = EasyID3(song.get_path())

        if artist:
            audio['ARTIST'] = song.get_artist()
        if album_artist:
            audio['ALBUMARTIST'] = song.get_album_artist()
        if title:
            audio['TITLE'] = song.get_title()
        audio.save()
        return song

    @staticmethod
    def random_generated_song_with_artist_data_only():
        return Generator.random_generated_song(artist=True)

    @staticmethod
    def random_generated_song_with_album_artist_data_only():
        return Generator.random_generated_song(album_artist=True)

    @staticmethod
    def random_generated_song_with_title_data_only():
        return Generator.random_generated_song(title=True)

    @staticmethod
    def create_file(path):
        file = open(path, "w")
        file.close()

    @staticmethod
    def random_bool():
        return random.choice([True, False])

    @staticmethod
    def random_songs_of_artists(artists):
        songs = []
        for artist in artists:
            for i in range(random.randint(2,3)):
                bool = Generator.random_bool()
                song = Generator.random_generated_song(bool, not bool, Generator.random_bool())
                song.set_artist(artist.get_name())
                songs.append(song)

        return songs

    @staticmethod
    def random_song_list(artist = False, album_artist = False, title = False):
        songs = []
        for i in range(Generator.random_int()):
            songs.append(Generator.random_song(artist, album_artist, title))
        return songs

    @staticmethod
    def random_artist():
        return Artist(Generator.random_genre(), f"RandomArtist{Generator.random_big_int()}")

    @staticmethod
    def random_generated_artist():

        genre = Generator.random_generated_genre()
        artist = Artist(genre, f"RandomArtist{Generator.random_big_int()}")
        f.create_directory(artist.get_path())
        return artist

    @staticmethod
    def random_generated_artists():
        artists = Generator.random_artists()
        for artist in artists.get_all_artists():
            try:
                f.create_directory(artist.get_genre().get_path())
            except:
                pass
            f.create_directory(artist.get_path())
        return artists

    @staticmethod
    def random_artist_with_specific_genre(genre):
        return Artist(genre, f"RandomArtist{Generator.random_big_int()}")

    @staticmethod
    def random_artists_dict():
        genres = dict()
        for i in range(random.randint(1,3)):
            genre = Generator.random_genre()
            artists = []
            for x in range(random.randint(1,4)):
                while True:
                    artist = Generator.random_artist_with_specific_genre(genre)
                    n = artist.get_name()
                    if n not in artists:
                        break
                artists.append(artist)

            genres[genre] = artists
        return genres

    @staticmethod
    def random_artists():
        return Artists(genres_path, Generator.random_artists_dict())

    @staticmethod
    def random_path():
        return Generator.random_string()+"\\"+Generator.random_string()

    @staticmethod
    def random_action_dict():
        actions = dict()

        for i in range(random.randint(1,100)):

            action = Generator.random_action()
            try:
                array = actions[action.get_type()]
            except:
                array = []
            array.append(action)
            actions[action.get_type()] = array

        return actions

    @staticmethod
    def random_history():
        h = History()
        count = random.randint(1,15)
        for i in range(count):
            h.add_action(Generator.random_action_list())
            h.next_index()
        return h

    @staticmethod
    def random_action_list():
        actions = []
        for i in range(Generator.random_int()):
            actions.append(Generator.random_action())

        return actions

    @staticmethod
    def random_action():
        types = [ActionType.MOVE, ActionType.CREATE, ActionType.DELETE]
        r = types[random.randint(0, 2)]
        if r == ActionType.MOVE:
            return ActionMove(Generator.random_path(), Generator.random_path())
        else:
            return ActionCreate(r, Generator.random_path())

    @staticmethod
    def random_action_with_type(type):
        return ActionCreate(type, Generator.random_path(), Generator.random_path())

    @staticmethod
    def random_move_action():
        return Generator.random_action_with_type(ActionType.MOVE)

    @staticmethod
    def random_action_list_with_type(type):
        list = []
        for i in range(random.randint(1,88)):
            list.append(Generator.random_action_with_type(type))

        return list

    @staticmethod
    def random_generated_song_list(artist = False, album_artist = False, title = False):
        songs = Generator.random_song_list(artist, album_artist, title)
        for song in songs:
            f.create_file(song.get_path())
        return songs

    @staticmethod
    def random_generated_song_of_known_artist(artist):
        song = Generator.random_generated_song()
        song.set_artist(artist.get_name())
        song.set_album_artist(artist.get_name())
        return song


