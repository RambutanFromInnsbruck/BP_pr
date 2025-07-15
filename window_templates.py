from tkinter import *
from variables import *

class DialogueWindow():
    CIPHER_TYPES = []

    def __init__(self, parent, title):
        self.root = Toplevel(parent)
        self.parent = parent
        self.vars = Vars()
        self.root.title(title)
        self.root.geometry("300x400")
        self.draw_widgets()
        self.grab_focus()

    def draw_widgets(self):
        self.search_entry = Entry(self.root)
        self.label = Label(self.root, text="Choose result:")
        self.choise = IntVar()

        self.cipher_instances = []
        self.search_entry.pack()
        self.label.pack()
        for idx, (cipher_cls, cipher_name) in enumerate(self.CIPHER_TYPES):
            cipher_obj = cipher_cls(self.parent)
            cipher_obj.set_cipher_window(self)

            Radiobutton(
                self.root,
                text=cipher_name,
                variable=self.choise,
                value=idx,
                command=cipher_obj.execute
            ).pack()

            self.cipher_instances.append(cipher_obj)

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()