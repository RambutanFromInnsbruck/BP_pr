import tkinter as tk
from tkinter import *
from tkinter import ttk
import re


class BlankTab():
    def __init__(self, parent):
        self.parent = parent
        self.tab_frame = None

        if not hasattr(parent, 'tab_counters'):
            parent.tab_counters = {}

    def set_riddle_window(self, riddle_window):
        self.riddle_window = riddle_window

    def draw_tab_w_cls_btn(self, tab_type: str):
        if tab_type not in self.parent.tab_counters:
            self.parent.tab_counters[tab_type] = 0
        self.parent.tab_counters[tab_type] += 1
        name = f"{tab_type} {self.parent.tab_counters[tab_type]}"
        self.tab_frame = Frame(self.parent.tabs_control)
        self.parent.tabs_control.add(self.tab_frame, text=name)
        self.parent.tabs_control.select(self.tab_frame)
        self.btn_cls = Button(self.tab_frame, width=2, height=1, relief=GROOVE, text="x",
                                     command=lambda: self.parent.tabs_control.forget(self.parent.tabs_control.select()))
        self.btn_cls.pack(anchor='ne')

    def validate(self, event, regex_pattern):
        if event.keysym in ('BackSpace', 'Delete', 'Return', 'Escape'):
            return
        if event.char:
            if not re.match(regex_pattern, event.char):
                return "break"


class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            CustomNotebook.__initialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element = self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def _draw_x_on_image(self, img, color):
        """Draw a thick X shape on a PhotoImage with the specified color"""

        start = 4

        for i in range(7):
            # First diagonal (top-left to bottom-right) - main line
            img.put(color, to=(start + i, start + i, start + i + 1, start + i + 1))
            # First diagonal - thickness (parallel lines)
            img.put(color, to=(start + i + 1, start + i, start + i + 2, start + i + 1))
            # Second diagonal (top-right to bottom-left) - main line
            img.put(color, to=(start + 7 - i, start + i, start + 8 - i, start + i + 1))
            # Second diagonal - thickness (parallel lines)
            img.put(color, to=(start + 6 - i, start + i, start + 7 - i, start + i + 1))

    def _create_close_button_images(self):
        """Create close button images programmatically"""
        size = 16

        # Create the three states with different colors
        img_close = tk.PhotoImage("img_close", width=size, height=size)
        self._draw_x_on_image(img_close, "#666666")  # Normal state - gray

        img_closeactive = tk.PhotoImage("img_closeactive", width=size, height=size)
        self._draw_x_on_image(img_closeactive, "#A19D37")  # Active state - yellow

        img_closepressed = tk.PhotoImage("img_closepressed", width=size, height=size)
        self._draw_x_on_image(img_closepressed, "#FF0000")  # Pressed state - red

        return (img_close, img_closeactive, img_closepressed)

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = self._create_close_button_images()

        style.element_create("close", "image", "img_close",
                             ("active", "pressed", "!disabled", "img_closepressed"),
                             ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])
