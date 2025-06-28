from tkinter import *

class HelpWindow():
    def __init__(self, parent):
        self.root = Toplevel(parent)
        self.parent = parent
        self.init()

    def init(self):
        self.root.title("Help")
        self.root.geometry("500x600")
        self.draw_widgets()

    def draw_widgets(self):
        self.label = Label(self.root, text="Babylonian pandemonium")
        self.label.pack()