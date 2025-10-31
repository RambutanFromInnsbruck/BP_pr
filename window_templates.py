from tkinter import *
from tkinter.messagebox import showinfo
from variables import *
from custom_widgets import AutocompleteEntry


class ChildWindow():
    def __init__(self, parent, title, width, height):
        self.root = Toplevel(parent)
        self.parent = parent
        self.init(title, width, height)
        self.position_child_window()

    def init(self, title, width, height):
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.draw_widgets()

    def position_child_window(self):
        self.root.update_idletasks()

        child_width = self.root.winfo_width()
        child_height = self.root.winfo_height()

        main_width = self.parent.winfo_width()
        main_height = self.parent.winfo_height()
        current_x = self.parent.winfo_x()
        current_y = self.parent.winfo_y()

        x = current_x + (main_width - child_width) // 2
        y = current_y + (main_height - child_height) // 2

        self.root.geometry(f"+{x}+{y}")

class DialogueWindow(ChildWindow):
    CONCEALMENT_TYPES = []

    def __init__(self, parent, title):
        self.vars = Vars()
        super().__init__(parent, title, 300, 400)

        self.grab_focus()

    def draw_widgets(self):
        self.search_entry = AutocompleteEntry(self.root)
        self.label = Label(self.root, text="Choose result:")
        self.choise = IntVar()

        self.concealment_instances = []

        search_list = [name for _, name in self.CONCEALMENT_TYPES]
        self.search_entry.set_completion_list(search_list)

        self.search_entry.pack()
        self.label.pack()

        self.search_entry.bind('<Return>', self.execute_from_srch)

        for idx, (concealment_cls, concealment_name) in enumerate(self.CONCEALMENT_TYPES):
            concealment_obj = concealment_cls(self.parent)
            concealment_obj.set_riddle_window(self)

            Radiobutton(
                self.root,
                text=concealment_name,
                variable=self.choise,
                value=idx,
                command=concealment_obj.execute
            ).pack()

            self.concealment_instances.append(concealment_obj)

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

    def execute_from_srch(self, *event):
        entered_name = self.search_entry.get()
        for idx, (concealment_cls, concealment_name) in enumerate(self.CONCEALMENT_TYPES):
            if concealment_name == entered_name:
                concealment_obj = self.concealment_instances[idx]
                concealment_obj.execute()

                break
        else:
            showinfo("Cipher Not Found",
                                f"No cipher named '{entered_name}' found.\n"
                                "Please select from the list or use autocomplete.")
