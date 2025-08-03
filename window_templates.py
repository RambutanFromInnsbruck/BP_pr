from tkinter import *
from tkinter.messagebox import showinfo
from variables import *
from custom_widgets import AutocompleteEntry

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
        self.search_entry = AutocompleteEntry(self.root)
        self.label = Label(self.root, text="Choose result:")
        self.choise = IntVar()

        self.cipher_instances = []

        search_list = [name for _, name in self.CIPHER_TYPES]
        self.search_entry.set_completion_list(search_list)

        self.search_entry.pack()
        self.label.pack()

        self.search_entry.bind('<Return>', self.execute_from_srch)

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

    def execute_from_srch(self, *event):
        entered_name = self.search_entry.get()
        for idx, (cipher_cls, cipher_name) in enumerate(self.CIPHER_TYPES):
            if cipher_name == entered_name:
                cipher_obj = self.cipher_instances[idx]
                cipher_obj.execute()

                break
        else:
            showinfo("Cipher Not Found",
                                f"No cipher named '{entered_name}' found.\n"
                                "Please select from the list or use autocomplete.")