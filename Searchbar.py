from tkinter import StringVar, Entry, Listbox, Button

from settings.settings_program import artist_width as aw


class Searchbar:
    def __init__(self, scroll_view, app, frame, list=[], when_item_selected_func=lambda x, y: None, state="normal", width=20, frm = None):
        self.frm = frm
        self.app = app
        self.scroll_view = scroll_view
        self.itemInListboxSelected = False
        self.element_list = list
        self.max_element_to_display = 5
        self.list_to_display = self.element_list
        self.var = StringVar()
        self.var.trace("w", lambda name, index, mode, x=self.var: self.on_text_change())
        self.entry = Entry(frame,textvariable=self.var, highlightthickness=2, state=state, width=width)
        self.when_item_selected_func = when_item_selected_func
        self.listbox = None
        self.old_value = ""
        if state == "readonly":
            self.readOnly = True
        else:
            self.readOnly = False

    def set_list(self, list):
        self.element_list = list

    def setScrollView(self, view):
        self.scrollView = view

    def getScrollView(self):
        return self.scrollView

    def on_app_click(self, widget):
        if widget == self.entry and self.entry.focus_get():
            self.create_listbox()
        else:
            self.delete_listbox()

    def on_text_change(self):
        if self.entry.focus_get():
            self.maybe_update_display_listbox()
            self.scroll_view.clear()
            w = int(aw * self.frm.get_width_percent())
            self.scroll_view.add_items(self.list_to_display, w)

    def maybe_create_listbox(self):
        if (self.listbox != None):
            return
        new_list = self.get_new_list(self.var.get(), self.element_list)
        if (len(new_list) <= 2):
            return

        self.create_listbox()

    def get_new_list(self, string_given, artists_list):
        if self.readOnly: return self.element_list
        new_list = []
        string_given_lower = string_given.lower()
        for artist in artists_list:
            string_lower = artist.get_name().lower()
            if (len(string_given) <= len(artist.get_name())):
                if (string_lower.find(string_given_lower) != -1):
                    new_list.append(artist)
        return new_list

    def maybe_update_display_listbox(self):
        new_value = self.var.get()
        if self.old_value == new_value:
            return
        else:
            self.old_value = new_value

        #returns a list of artists
        possible_new_list_to_display = self.get_new_list(new_value, self.element_list)

        if (len(possible_new_list_to_display) == 0):
            # print("nothing to display")
            self.m_list_to_display = possible_new_list_to_display
            if (self.listbox != None):
                self.delete_listbox()
            else:
                pass
                # print("La listbox n'existe déjà plus")
            return

        elif possible_new_list_to_display == self.list_to_display:
            # print("list are the same, no need to update")
            if (self.listbox != None):
                pass
                # print("There is already a list so it's ok")
            else:
                self.create_listbox()
                # print("error: listbox should already exist cause length is more than 0...")
            return

        elif (len(possible_new_list_to_display) == len(self.list_to_display)):
            # print("just need to update the values, not the length")
            self.list_to_display = possible_new_list_to_display
            if (self.listbox != None):
                self.update_display_list()
            else:
                # print("error: listbox should have already been created.")
                self.create_listbox()
            return
        elif (len(possible_new_list_to_display) >= self.max_element_to_display and
              len(self.list_to_display) >= self.max_element_to_display):
            # print("not the same len but we are gonna display the max number of row anyway")
            self.list_to_display = possible_new_list_to_display
            if (self.listbox != None):
                self.update_display_list()
            else:
                if not (self.itemInListboxSelected):
                    print("error: listbox should have already been created....")
                    self.create_listbox()

            return
        # print("we have to change the length of the LISTBOX display (and the values)")
        self.list_to_display = possible_new_list_to_display
        if (self.listbox != None):
            self.delete_listbox()
        self.create_listbox()

    def item_selected(self, event):
        self.itemInListboxSelected = True
        selected_item_tuple_id = self.listbox.curselection()
        if (selected_item_tuple_id == ()):
            return
        idx = selected_item_tuple_id[0]
        string = str(self.listbox.get(self.listbox.curselection()))
        self.var.set(string)
        self.delete_listbox()
        self.when_item_selected_func(idx, string)

    def update_display_list(self):
        if (self.listbox == None):
            # print("error: listbox should exist before calling this function...")
            return
        self.listbox.delete(0, "end")
        for string in self.list_to_display: self.listbox.insert('end', string)

    def set_value(self, value):
        try:
            self.var.set(value)
            self.delete_listbox()
        except Exception as e:
            print("SearchBar.py l159")
            print(value)
            print(e)

    def create_listbox(self):
        # print("we create the listbox")
        if (self.listbox != None):
            # print("error: list should have been absent")
            return

        #returns a list of artists
        new_list = self.get_new_list(self.var.get(), self.element_list)

        if (len(new_list) == 0):
            # print("kind of error: We shouldn't try to display an empty listbox")
            return

        self.list_to_display = new_list

        # self.app.update()
        self.update_display_list()
        # print(self.element_list)
        # print(self.list_to_display)

    def delete_listbox(self):
        if (self.listbox == None):
            # print("error: list should have been present")
            return
        self.listbox.unbind('<<ListboxSelect>>')
        self.listbox.delete(0, "end")
        self.listbox.destroy()
        del self.listbox
        self.listbox = None
        self.list_to_display = []
        self.itemInListboxSelected = False
