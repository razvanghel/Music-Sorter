import time
from tkinter import *

from handlers.GUIHandler import GUIHandler
from model.frame.FrameTemplate import FrameTemplate
from model.song import SongViewSettings
from model.sounds.sound_type import SoundType


class SongsFrame(FrameTemplate):

    def __init__(self, master, *pargs, mode = SoundType.SONG):
        super().__init__(master, *pargs, mode)
        self.tick_vars = []

    def get_ticked_songs(self):
        result = list()
        for var in self.tick_vars:
            if var.get():
                index = self.tick_vars.index(var)
                result.append(self.get(index))
        return result

    def get_song(self, var):
        return self.get(self.tick_vars.index(var))

    def tick_all(self):
        self._set(True)

    def _set(self, bool):
        for i in range(0, len(self.tick_vars)):
            self.tick_vars[i].set(bool)

    def clear_command(self):
        self._set(False)

    def delete(self):
        songs = self.get_ticked_songs()
        self.remove_songs(songs)

    def _binary_search_greater_or_equal(self, low, high, song):

        if low <= high:
            mid = int((high + low) / 2)
            if self.get(mid - 1).get_name() <= song.get_name() and song.get_name() < self.get(mid).get_name():
                return mid
            elif self.get(mid).get_name() < song.get_name():
                return self._binary_search_greater_or_equal(mid + 1, high, song)
            else:
                return self._binary_search_greater_or_equal(low, mid - 1, song)

        return None

    def _linear_search(self, song):
        for s in self.get_items_list():
            if s.get_name() > song.get_name():
                return self.get_items_list().index(s)
        return self.get_size()

    def _get_song(self, name):
        for song in self.get_items_list():
            if song.get_name() == name:
                return song

    def create_item(self, song, width, index=None):
        if self.mode == SoundType.SONG:
            return self._create_song_gui(song, width, index)
        else:
            return self._create_sound_gui(song, width, index)


    def add_song(self, index, song, width):
        self.items_list.insert(index, song)
        button = self.create_item(song, width, index)
        self.add_button(button, index)

    def add_button(self, button, row):
        self.gui_list.insert(row, button)
        if row < self.row:
            self._move_down(row)
        button.grid(row=row + 1)

    def _move_down(self, row):
        for r in range(self.row, row, -1):
            self.get_gui(r).grid(row=r + 1)

    def _add_item(self, song, width):
        index = self._linear_search(song)
        song.set_name(self._check_name(song.get_name()))
        self.add_song(index, song, width)

    def _check_name(self, name):
        extension = self._get_extension(name)
        name = name[:len(name) - len(extension)]
        if name in self.get_songs_names_list():
            return self._check_name(name + "(1)" + extension)
        return name + extension

    def remove_songs(self, songs):
        for song in songs:
            self._remove_song(song)
        self.update()

    def clear(self):
        i = len(self.tick_vars) -1
        while i>=0:
            self.remove_item(i)
            i-=1
        self.tick_vars = []

    def get_songs_names_list(self):
        result = list()
        for song in self.get_items_list():
            result.append(song.get_name())
        return result

    def _get_extension(self, name):
        array = name.split(".")
        return "." + array[-1]

    def _remove_song(self, song):
        index = self.get_items_list().index(song)
        r = self.tick_vars[index]
        self.tick_vars.remove(r)
        self.remove_item(index)
        self.row -= 1
        self.update()


    def _create_sound_gui(self, sound, width, index = None):
        label = Label(self, font='2', height=2, width=width + 40, text=sound.get_name())
        var = BooleanVar()
        check_button = Checkbutton(label, variable=var, onvalue=1, offvalue=0)
        self.tick_vars.insert(index, var)
        GUIHandler.place_label(check_button, 0.95, SongViewSettings.y, .05, SongViewSettings.height)
        return label

    def _create_song_gui(self, song, width, index):
        label = Label(self, font='2', height=2, width=width + 40)
        file = Button(label, text=f"File:\n{song.get_name()}")
        title = Button(label, text=f"Title:\n{song.get_title()}")
        artist = Button(label, text=f"Artist:\n{song.get_artist()}")
        contributing_artist = Button(label, text=f"Album artist:\n{song.get_album_artist()}")

        var = BooleanVar()
        check_button = Checkbutton(label, variable=var, onvalue=1, offvalue=0)
        self.tick_vars.insert(index, var)

        w = SongViewSettings.width
        height = SongViewSettings.height
        y = SongViewSettings.y

        GUIHandler.place_label(file, w * 0, y, 0.5, height)
        GUIHandler.place_label(title, 0.5, y, 0.15, height)
        GUIHandler.place_label(artist, 0.65, y, 0.15, height)
        GUIHandler.place_label(contributing_artist, 0.8, y, 0.15, height)
        GUIHandler.place_label(check_button, 0.95, y, .05, height)
        return label
