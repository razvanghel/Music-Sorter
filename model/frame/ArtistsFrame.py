from tkinter import Button
import copy
from model.frame.FrameTemplate import FrameTemplate
from model.frame.SongsFrame import SoundType
from model.top_buttons.AddUndo import AddUndo


class ObjectHoldingTheValue:
    def __init__(self, initial_value=None):
        self._value = initial_value
        self._callbacks = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        old_value = self._value
        self._value = new_value
        self._notify_observers(old_value, new_value)

    def _notify_observers(self, old_value, new_value):
        for callback in self._callbacks:
            callback(old_value, new_value)

    def register_callback(self, callback):
        self._callbacks.append(callback)




class ArtistsFrame(FrameTemplate):


    def check_artists(self, old_value, new_value):
        if old_value != new_value:
            self.button.config(text = "Add to: {a}\n(ENTER)".format(a=new_value))

    def __init__(self, master, *pargs, mode = SoundType.SONG):
        FrameTemplate.__init__(self, master, *pargs)
        self.holder = ObjectHoldingTheValue()
        self.holder.register_callback(self.check_artists)
        self.mode = mode

    def create_item(self, artist, width, index = None):
        return Button(self, fg='black', font='23', text=artist.get_name(), height=2, width=width, padx=1, command = lambda: self._set_current_artist(artist.get_name()))

    def _set_current_artist(self, name):
        self.holder.value = name

    def get_current_artist(self):
        return self.holder.value

    def set_add_button(self, button):
        self.button = button

    def get_button(self):
        return self.button
