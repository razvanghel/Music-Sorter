from tkinter import *

from settings import settings_program


class fFrame(Frame):

    def __init__(self, screen_width, screen_height, master, *pargs):
        Frame.__init__(self, master, *pargs)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bind('<Configure>', self._resize_buttons)
        self.buttons_frame = None
        self.song_frame = None

    def get_screen_width(self):
        return self.screen_width

    def get_screen_height(self):
        return self.screen_height

    def get_width_percent(self):
        return self.winfo_width() / self.screen_width

    def get_width_percentage(self, current_width, songs = False):
        if songs == False:
            return int(settings_program.artist_width * current_width / self.screen_width)
        else:
            return int(settings_program.song_width * current_width / self.screen_width)

    def get_width_p(self, songs = False):
        current_width = self.winfo_width()
        if songs == False:
            return int(settings_program.artist_width * current_width / self.screen_width)
        else:
            return int(settings_program.song_width * current_width / self.screen_width)

    def resize_buttons(self, songs = True):
        current_width = self.winfo_width()
        w = self.get_width_percentage(current_width, songs)
        if self.buttons_frame != None:
            for button in self.buttons_frame.get_gui_list():
                button.config(width = w)

        if self.song_frame != None:
            for song in self.song_frame.get_gui_list():
                song.config(width = w)


    def _resize_buttons(self, event):

        if self.buttons_frame != None:
            w = self.get_width_percentage(event.width)
            for button in self.buttons_frame.get_gui_list():
                button.config(width = w)

        if self.song_frame != None:
            w = self.get_width_percentage(event.width, True)
            for song in self.song_frame.get_gui_list():
                song.config(width = w)

    def set_buttons_frame(self, frame):
        self.buttons_frame = frame

    def set_song_frame(self, frame):
        self.song_frame = frame

    def get_buttons_frame(self):
        return self.buttons_frame

