from tkinter import *

class MyListbox(Listbox):

    _ARTIST_WEIGHT = 20
    _FILE_NAME_WEIGHT = 35
    _TITLE_WEIGHT = 35
    _CHECKBOX_WEIGHT = 10

    def __init__(self, master=None, cnf={}, **kw):
        Widget.__init__(self, master, 'listbox', cnf, kw)
        # Listbox.__init__()
        # self._create_top_label()

    def _create_top_label(self):
        self.top_label = Label(self)