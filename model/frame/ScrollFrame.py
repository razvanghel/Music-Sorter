
from tkinter import Frame, Canvas, Scrollbar

from handlers.GUIHandler import GUIHandler
from model.frame.ArtistsFrame import ArtistsFrame
from model.frame.FrameTemplate import FrameTemplate
from model.frame.FrameType import FrameType
from model.frame.SongsFrame import SongsFrame


class ScrollFrame(Frame):

    def __init__(self, type, master, *pargs, mode = None):
        Frame.__init__(self, master, *pargs)

        self.root = master

        self.canvas = Canvas(self.root, bg='blue')
        self.scrollbar = Scrollbar(self.root, command=self.canvas.yview)

        if type == FrameType.ARTISTS:
            self._frame = ArtistsFrame(self.canvas, mode = mode)
        elif type == FrameType.SONGS:
            self._frame = SongsFrame(self.canvas, mode = mode)

        self.type = type
        self.canvas.create_window((0,0), window = self._frame, anchor ="nw")
        self.configure()

    def configure(self):
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def get_canvas(self):
        return self.canvas

    def get_songs_or_artists_frame(self):
        return self._frame

    def get_type(self):
        return self.type
    def get_scrollbar(self):
        return self.scrollbar

    def add_buttons_with_width(self, list, width):
        self._frame.add_items(list, width)

    def add_buttons(self, list):
        self.update()
        self._frame.add_items(list, 161)

    def get_root(self):
        return self.root

    def update_canvas(self):
        canvas = self.canvas
        self.canvas.destroy()
        self.canvas = canvas

    def change_mode(self):
        self._frame.change_mode()
