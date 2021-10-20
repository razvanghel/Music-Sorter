from tkinter import Button, Label


class GUIHandler():
    @staticmethod
    def place_label(label, relX, relY, relWidth, relHeight):
        label.place(relx=relX, rely=relY, relwidth=relWidth, relheight=relHeight)

    @staticmethod
    def create_button(text):
        return Button(fg='black', font='23', text=text, height=2, width=100, padx=1)
