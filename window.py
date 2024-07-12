from tkinter import *
from tkinter.ttk import Notebook
from cipher_diaolgue import Cipher_window

class Window:
    def __init__(self):
        self.root = Tk()
        self.init()

    def init(self):
        self.root.title("Babylonian pandemonium")
        self.root.geometry("700x500")

        self.root.bind('<F1>', self.help)
        self.root.bind('<F11>', self.fullscreen)
        self.root.bind("<Escape>", self._close)

    def run(self):
        self.draw_menu()
        self.draw_widgets()
        self.root.mainloop()

    # needs to draw help win
    def draw_menu(self):
        main_menu = Menu(self.root)
        tools_menu = Menu(main_menu, tearoff=0)
        ciphers_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Tools", menu=tools_menu)
        main_menu.add_command(label="Help", command=self.help)
        tools_menu.add_cascade(label="Cryptography", menu=ciphers_menu)
        tools_menu.add_command(label="Steganography", command=self.func)
        ciphers_menu.add_command(label="Encode", command=self.dialogue_window)
        ciphers_menu.add_command(label="Decode", command=self.dialogue_window)

        self.root.configure(menu=main_menu)

    def draw_widgets(self):
        self.root.tabs_control = Notebook(self.root)
        self.root.tabs_control.pack(expand=1, fill='both')

    def dialogue_window(self):
        Cipher_window(self.root)

    def help(self, *event):
        print("Help was clicked")

    def func(self):
        print("Stego was clicked")

    def fullscreen(self, event):
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
        else:
            self.root.attributes('-fullscreen', True)

    def _close(self, event):
        self.root.quit()

if __name__ == "__main__":
    Window().run()