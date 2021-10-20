import os
from tkinter import Label, Entry, Button

from tkdnd import TixTk
from handlers import FileHandler as f
from handlers.GUIHandler import GUIHandler

song_width = 140
artist_width = 61


file = "settings.txt"
def read_artist():
    if f.exists(file):
        fil = read_file()
        artist = fil.readline()
        artist = artist.replace("\n", "")
        return artist
    return ""

def read_sound():
    if f.exists(file):
        ff = read_file()
        ff.readline()
        sound = ff.readline()
        sound = sound.replace("\n", "")
        return sound
    return ""

def read_file():
    f = open(os.path.abspath(file))
    return f

def write(string):
    f = open(os.path.abspath(file), "w")
    f.write(string)

class Settings:
    def __init__(self):
        if not f.exists(file):
            self.read_file()
        else:
            self.artistPath = read_artist()
            self.soundsPath = read_sound()

    def get_artists_path(self):
        return self.artistPath

    def get_sounds_path(self):
        return self.soundsPath

    def change_artists_path(self, path):
        self.artistPath = path
        string = f"{path}\n{self.soundsPath}\n"
        write(string)

    def change_sounds_path(self, path):
        self.soundsPath = path
        string = f"{self.artistPath}\n{path}\n"
        write(string)

    def read_file(self):
        try:
            f = open(os.path.abspath(file))
            return f
        except:
            self.root = TixTk()
            self.root.geometry(f"{int(self.root.winfo_screenwidth() / 2)}x{int(self.root.winfo_screenheight() / 2)}")
            label = Label(self.root, bg='grey')
            GUIHandler.place_label(label, 0, 0, 1, 1)
            text = Label(label, text="Paths not found. Please add the desired path to the following:")
            GUIHandler.place_label(text, 0.15, 0.1, 0.7, 0.1)

            self.path_text = Label(label, text="Artists path:", bg='grey')
            GUIHandler.place_label(self.path_text, 0.15, 0.5, 0.7, 0.1)
            self.entry = Entry(label)
            GUIHandler.place_label(self.entry, 0.15, 0.6, 0.7, 0.1)

            self.ok = Button(label, text="OK", command=lambda: self._to_artists_path())
            GUIHandler.place_label(self.ok, 0.35, 0.88, 0.3, 0.1)
            self.root.mainloop()


    def _to_artists_path(self):
        self.artistPath = self.entry.get()
        self.entry.setvar("")
        self.path_text.config(text="Sounds path:")
        self.ok.config(command = lambda : self._to_sounds_path())

    def _to_sounds_path(self):

        self.change_sounds_path(self.entry.get())
        self.entry.setvar("")
        self.ok.config(command = lambda : self.root.destroy())

s = Settings()
artists_path = s.get_artists_path()
sounds_path = s.get_sounds_path()