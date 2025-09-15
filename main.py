from tkinter import *
from tkinter.messagebox import askokcancel
from dec_crypto_win import DecodeCipherWindow
from enc_crypto_win import EncodeCipherWindow
from custom_widgets import CustomNotebook
from help_win import HelpWindow


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
        self.root.protocol('WM_DELETE_WINDOW', self._close)
        self.root.mainloop()

    def draw_menu(self):
        main_menu = Menu(self.root)
        tools_menu = Menu(main_menu, tearoff=0)
        ciphers_menu = Menu(main_menu, tearoff=0)
        stego_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Tools", menu=tools_menu)
        main_menu.add_command(label="Help", command=self.help)
        tools_menu.add_cascade(label="Cryptography", menu=ciphers_menu)
        tools_menu.add_cascade(label="Steganography", menu=stego_menu)
        ciphers_menu.add_command(label="Encode", command=self.dialogue_cryptoencode_window)
        ciphers_menu.add_command(label="Decode", command=self.dialogue_cryptodecode_window)
        stego_menu.add_command(label="Encode", command=self.dialogue_stegoencode_window)
        stego_menu.add_command(label="Decode", command=self.dialogue_stegodecode_window)

        self.root.configure(menu=main_menu)

    def draw_widgets(self):
        self.root.tabs_control = CustomNotebook(self.root)
        self.root.tabs_control.pack(expand=1, fill='both')

    def dialogue_cryptoencode_window(self):
        EncodeCipherWindow(self.root)

    def dialogue_cryptodecode_window(self):
        DecodeCipherWindow(self.root)

    def dialogue_stegoencode_window(self):
        print("Stego was clicked")

    def dialogue_stegodecode_window(self):
        print("Stego was clicked")

    def help(self, *event):
        HelpWindow(self.root)

    def fullscreen(self, event):
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
        else:
            self.root.attributes('-fullscreen', True)

    def _close(self, *event):
        choice = askokcancel("Quit", "Do you want to quit?")
        if choice:
            self.root.quit()


if __name__ == "__main__":
    Window().run()
