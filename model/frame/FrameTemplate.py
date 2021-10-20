from abc import abstractmethod
from tkinter import *

from handlers.Reader import Reader
from model.sounds.sound_type import SoundType
from settings.settings_program import artists_path, Settings
from settings.settings_program import sounds_path


class FrameTemplate(Frame):


    def __init__(self, master, *pargs, mode = SoundType.SONG):
        Frame.__init__(self, master, *pargs)
        self.mode = mode
        self.update()
        self.root = master
        self.gui_list = list()
        self.items_list = list()
        self.row = 0

    def get_root(self):
        return self.root

    def get_mode(self):
        return self.mode

    def get_frame(self):
        return self.winfo_children()

    @abstractmethod
    def add_button(self, button, row):

        self.gui_list.append(button)
        button.grid(row=row)

    def insert(self, item, index):
        self.items_list.insert(item, index)


    def get_gui_list(self):
        return self.gui_list

    def get_items_list(self):
        return self.items_list

    def get_size(self):
        return len(self.gui_list)

    def get(self, index):
        return self.items_list[index]

    def get_gui(self, index):
        return self.gui_list[index]

    def _is_in_list(self, item):
        for check in self.items_list:
            if check.get_name() == item.get_name() and check.get_path() == item.get_path():
                return True
        return False

    def _not_in_list(self, item):
        return not self._is_in_list(item)

    def _increase_row(self):
        self.row +=1

    def _decrease_row(self):
        self.row -=1

    def _set_row(self, row):
        self.row = row

    def change_mode(self):
        self.mode = SoundType.other(self.mode)
        self.clear()

    def _get_width_percentage(self, current_width):
        return int(Settings.artist_width * current_width / self.screen_width )

    def add_items(self, list, width=None):
        self.update()
        for item in list:
            if self._not_in_list(item):
                self._add_item(item, width)
                self._increase_row()

    @abstractmethod
    def create_item(self, item, width, index = None):
        pass

    def get_removable_items(self):
        return self.get_gui_list()[1:len(self.get_gui_list())]

    @abstractmethod
    def clear(self):
        self.row = 0
        for item in self.get_gui_list():
            item.destroy()
        self.items_list.clear()
        self.gui_list.clear()

    def remove_item(self, index):
        gui = self.gui_list[index]
        self.gui_list.remove(gui)
        self.items_list.remove(self.items_list[index])
        gui.destroy()

    @abstractmethod
    def _add_item(self, item, width):
        self.add_button(self.create_item(item, width), self.row)
        self.items_list.append(item)
