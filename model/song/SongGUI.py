from tkinter import *

from tinytag import TinyTag

from handlers import FileHandler as f
from model.song.Song import Song


class SongGUI(Song):

    def __init__(self, root, path, width):
        try:
            audio = TinyTag.get(path)
            Song.__init__(self, path, artist = audio.artist, file_name= f.extract_from_path(path), title = audio.title, album_artist= audio.albumartist, genre=audio.genre)
        except:
            Song.__init__(self, path, file_name = f.extract_from_path(path), artist="", title="", album_artist="")


    def is_ticked(self):
        return self.tick_var

    def tick(self):
        self.tick_var = not self.tick_var