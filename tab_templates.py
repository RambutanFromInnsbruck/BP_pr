from tkinter import *
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
        self.btn_cls = Button(self.tab_frame, width=2, height=1, relief=GROOVE, text="x", font=('Arial', 11),
                              command=lambda: self.parent.tabs_control.forget(self.parent.tabs_control.select()))
        self.btn_cls.pack(anchor='ne')

    def validate(self, event, regex_pattern):
        if event.keysym in ('BackSpace', 'Delete', 'Return', 'Escape'):
            return
        if event.char:
            if not re.match(regex_pattern, event.char):
                return "break"
