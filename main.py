import time
from threading import Thread
from tkinter import *

from tkinterdnd2 import DND_FILES
from tkinterdnd2.TkinterDnD import *

from handlers.GUIHandler import GUIHandler
from model.artists.Artists import Artists
from Searchbar import Searchbar
from handlers.Reader import Reader
from model.frame.FrameType import FrameType
from model.frame.ScrollFrame import ScrollFrame
from model.frame.SongsFrame import SoundType
from model.top_buttons.AddUndo import AddUndo
from settings import settings_program
from settings.settings_program import Settings
from settings.settings_program import artists_path
from settings.settings_program import sounds_path
from handlers.Frame import Frame, fFrame
from model.song import SongViewSettings

s = Settings()
class Gui:
    root = TixTk()
    root.title("MusicSorter")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width-400}x{screen_height-440}')
    root.configure(background="black")
    drag_list = tkinter.Listbox(root, selectmode = tkinter.SINGLE, background = "#ffe0d6")



    def __init__(self):
        self.frm = fFrame(self.screen_width, self.screen_height, self.root)
        self.frm.pack(fill=BOTH, expand=YES)
        self.initiate()
        self.root.state('zoomed')

        # self._change_mode()

    def drop_inside_list_box(self,event):

            songs = Reader.read_songs(self.drag_list,event.data, self.frm.get_width_percentage(self.frm.winfo_width()))
            width = 100
            w = width

            if self.songs_frame == None:
                songs_frame = ScrollFrame(FrameType.SONGS, self.drag_list, mode = self.mode)
                self.songs_scroll_frame = songs_frame
                self.songs_frame = songs_frame.get_songs_or_artists_frame()
                self.frm.set_song_frame(songs_frame.get_songs_or_artists_frame())
                songs_frame.add_buttons_with_width(songs, w)
                width = 0.97

                GUIHandler.place_label(songs_frame.get_scrollbar(), width, 0, 1 , 1)
                GUIHandler.place_label(songs_frame.get_canvas(), 0, 0, 1, 1)

            else:
                self.songs_frame.add_items(songs, w)
                self.frm.set_song_frame(self.songs_frame)

            self.update_gui()

    def update_gui(self):
        # self.root.state('normal')
        self.root.geometry(f"{self.root.winfo_width() + 1}x{self.root.winfo_height() + 1}")
        self.root.update()
        self.root.geometry(f"{self.root.winfo_width() - 1}x{self.root.winfo_height() - 1}")
        # self.root.state('zoomed')

    def createDragLabel(self, dragLabelX, dragLabelY, dragLabelWidth, dragLabelHeight):
        self.songs_frame = None
        self.drag_list = Listbox(self.frm, bg='white')

        self.button_h = 0.1
        self.drag_list.place(relx=dragLabelX, rely=dragLabelY, relwidth=dragLabelWidth, relheight=dragLabelHeight)
        # self.create_songs_label()



        self.drag_list.drop_target_register(DND_FILES)
        self.drag_list.dnd_bind("<<Drop>>", self.drop_inside_list_box)

        self.x = dragLabelX
        self.y = dragLabelY
        self.width = dragLabelWidth
        self.height = dragLabelHeight


    def createLabels(self):
        dragLabelY = .105
        drag_label_x = .0075
        dragLabelWidth = 0.68
        dragLabelHeight = .89


        self.createDragLabel(drag_label_x, dragLabelY, dragLabelWidth - drag_label_x, dragLabelHeight)
        self.mode = SoundType.SONG
        self.create_search_label(dragLabelWidth, dragLabelY, 0.3, dragLabelHeight)
        button_width = (1 - drag_label_x*3.6)/4
        self.createTopButtons(drag_label_x, (1-dragLabelHeight)*0.1, button_width, (1-dragLabelHeight)*0.8)

    def _send_sounds(self):
        songs = self.songs_frame.get_ticked_songs()
        a = self.artists_frame.get_current_artist()
        if a!=None:
            artist = self.artists.get_artist_by_name(a)
            self.add.add_songs(songs, artist)
            self.songs_frame.remove_songs(songs)
            self._add_report()


    def _auto_add(self):
        frame = self.songs_frame
        if frame != None:
            songs = frame.get_items_list()
            self.add.auto_add(self.artists, songs)
        self.songs_frame_clear()
        self.reset_check()
        self._add_report()

    def create_search_label(self, labelX, labelY, labelWidth, labelHeight):
        label = Label(self.frm, bg='red', fg="black")
        GUIHandler.place_label(label, labelX, labelY, labelWidth, labelHeight)

        a_dict = Reader.read_artists(s.get_artists_path())
        self.artists = Artists(s.get_artists_path(), a_dict)
        self.add = AddUndo()

        searchFrame = Frame(label, bg='red')
        searchbarHeight = 0.1

        self.artists_scroll_frame = ScrollFrame(FrameType.ARTISTS, searchFrame, mode = self.mode)
        buttons_frame = self.artists_scroll_frame.get_songs_or_artists_frame()

        self.searchbar = Searchbar(buttons_frame, label, label, self.artists.get_all_artists(), frm=self.frm)

        #set resize trigger
        self.frm.set_buttons_frame(buttons_frame)
        #add artists to the list
        self.artists_scroll_frame.get_songs_or_artists_frame().set_add_button(Button(self.root, text ="Add", command=self._send_sounds))
        self.artists_scroll_frame.add_buttons(self.artists.get_all_artists())
        self.artists_frame =  self.artists_scroll_frame.get_songs_or_artists_frame()

        button_h = 0.08
        button = Button(label, text="+", width=100)
        GUIHandler.place_label(searchFrame, 0, (searchbarHeight + button_h), 1, 0.9)

        width = 1 - SongViewSettings.scrollbar_width
        GUIHandler.place_label(self.artists_scroll_frame.get_scrollbar(), width, 0, 1 - width, 1 - button_h-.01)
        GUIHandler.place_label(self.artists_scroll_frame.get_canvas(), 0, 0, width, 1 - button_h-.01)

        GUIHandler.place_label(button, 0, searchbarHeight, 1.0025, button_h)
        GUIHandler.place_label(self.searchbar.entry, 0, 0, 1, searchbarHeight)

    def createTopButtons(self, drag_label_x, drag_label_y, button_width_percent, drag_label_height_percent):

        drag_label_height_percent /= 2
        undo = Button(self.root, text = "Undo", command = lambda : self.undo())
        auto_add = Button(self.root, text = "Auto add", command = lambda : self._auto_add())
        add = self.artists_frame.get_button()
        self.change_mode = Button(self.root, text =f"Switch mode to: {SoundType.other(self.mode)}", command = lambda : self._change_mode())
        settings = Button(self.root, text = "Settings", command = lambda : self._go_to_settings())
        clear = Button(self.root, text="Clear", command = lambda : self.songs_frame_clear())
        delete = Button(self.root, text="Delete", command = lambda : self.delete())
        select_all = Button (self.root, text = "Select All", command = lambda : self.select_all())



        GUIHandler.place_label(self.change_mode, drag_label_x, drag_label_y, button_width_percent, drag_label_height_percent)
        GUIHandler.place_label(settings, drag_label_x, drag_label_y + drag_label_height_percent, button_width_percent, drag_label_height_percent)

        GUIHandler.place_label(add, drag_label_x + button_width_percent, drag_label_y, button_width_percent, drag_label_height_percent)
        GUIHandler.place_label(select_all, drag_label_x + button_width_percent, drag_label_y + drag_label_height_percent, button_width_percent, drag_label_height_percent)

        GUIHandler.place_label(auto_add, drag_label_x + button_width_percent * 2, drag_label_y, button_width_percent, drag_label_height_percent)
        GUIHandler.place_label(clear, drag_label_x + button_width_percent * 2, drag_label_y + drag_label_height_percent, button_width_percent, drag_label_height_percent)


        GUIHandler.place_label(undo, drag_label_x + button_width_percent * 3, drag_label_y, button_width_percent, drag_label_height_percent)
        GUIHandler.place_label(delete, drag_label_x + button_width_percent * 3, drag_label_y + drag_label_height_percent, button_width_percent, drag_label_height_percent)

    def initiate(self):
        self.createLabels()

    def mainloop(self):
        self.root.mainloop()

    def delete(self):
        try:
            self.songs_frame.delete()
        except:
            pass
        self.reset_check()

    def reset_check(self):
        try:
            if len(self.songs_frame.get_ticked_songs()) == len(self.songs_frame.get_items_list()):
                self.songs_scroll_frame.get_canvas().destroy()
                self.songs_frame = None
        except:
            pass

    def select_all(self):
        try:
            self.songs_frame.tick_all()
        except:
            pass

    def songs_frame_clear(self):
        try:
            self.songs_frame.clear()
        except:
            pass

    def undo(self):
        try:
            self.add.undo()

        except:
            pass

    def _get_string(self, list):
        string = ""
        for item in list:
            string+=item.get_path()+"\n"
        return string

    def _add_report(self):
        string = ""
        if len(self.add.get_new_added_artists()):
            string += f"{len(self.add.get_new_added_artists())} artists were added.\n\n"
        if len(self.add.get_unsorted_songs()) > 0 :
            string += f"{len(self.add.get_unsorted_songs())} songs could not be sorted.\n\n"

        if string =="":
            string = "Files moved successfully."

        self._message_label(string)

    def _message_label(self, message):
        label = Label(self.frm, text=message, bg='grey')
        button = Button(label, text="OK", command=lambda: label.destroy())
        GUIHandler.place_label(button, 0.42, 0.84, 0.16, 0.15)
        x = 0.3
        y = 0.4
        GUIHandler.place_label(label, x, y, 1 - x * 2, 1 - y * 2)

    def _go_to_settings(self):
        label = Label(self.frm, bg='grey')
        self.entry = Entry(label, bg = 'white')
        change_sounds = Button(label, text = "Change", command = lambda : self._change_sounds())
        change_artist = Button(label, text = "Change", command = lambda : self._change_artist())
        self.text_artist = Label(label, bg ='grey', text =f"Artists path: {artists_path}", anchor ="w")
        self.text_sounds = Label(label, bg ='grey', text =f"Sounds path: {sounds_path}", anchor ="w")
        GUIHandler.place_label(self.text_artist, 0.1, 0.10, 0.4, 0.1)
        GUIHandler.place_label(change_artist, 0.01, 0.10, 0.08, 0.1)

        GUIHandler.place_label(change_sounds, 0.01, 0.30, 0.08, 0.1)
        GUIHandler.place_label(self.text_sounds, 0.1, 0.30, 0.4, 0.1)

        GUIHandler.place_label(self.entry, 0.3, 0.55, 0.4, 0.13)

        button = Button(label, text="OK", command= lambda: label.destroy())
        GUIHandler.place_label(button, 0.42, 0.84, 0.16, 0.15)
        x = 0.3
        y = 0.4
        GUIHandler.place_label(label, x, y, 1 - x * 2, 1 - y * 2)

    def _change_mode(self):
        self.mode = SoundType.other(self.mode)
        self.change_mode.config(text =f"Switch to: {self.mode}")
        if self.songs_frame != None:
            self.songs_frame.change_mode()
        if self.artists_scroll_frame != None:
            self.artists_scroll_frame.change_mode()
            list = self._check()
            self.artists_scroll_frame.add_buttons(list)
            self.searchbar.set_list(list)
            if self.root.state() == "zoomed":
                self.root.state('normal')
                self.update_gui()
                self.root.state('zoomed')
        self.update_gui()
        self.reset_check()



    def _check(self):
        if self.mode == SoundType.SOUND:
            return Reader.read_sounds_from_library(sounds_path)
        else:
            a =  Artists(s.get_artists_path(), Reader.read_artists(s.get_artists_path()))
            return a.get_all_artists()

    def _change_sounds(self):
        value = self.entry.get()
        s.change_sounds_path(value)
        self.text_sounds.config(text =f"Artists path: {s.get_sounds_path()}")

    def _change_artist(self):
        value = self.entry.get()
        s.change_artists_path(value)
        self.text_artist.config(text=f"Artists path: {s.get_artists_path()}")



gui = Gui()
gui.mainloop()

