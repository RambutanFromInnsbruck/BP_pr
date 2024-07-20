from tkinter import *
from tkinter.ttk import Notebook
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText
import re
import random
from variables import Vars


class CipherWindow():
    def __init__(self, parent):
        self.root = Toplevel(parent)
        self.parent = parent
        self.vars = Vars()
        self.init()

    def init(self):
        self.root.title("Dialogue")
        self.root.geometry("300x400")
        self.draw_widgets()
        self.grab_focus()

    def draw_widgets(self):
        self.search_entry = Entry(self.root)
        self.label = Label(self.root, text="Choose cipher:")
        self.choise = IntVar()

        self.gp = GrandPrix(self.parent)
        self.gp.set_cipher_window(self)
        self.radio_button_1 = Radiobutton(self.root, text="Grand Prix Cipher", variable=self.choise,
                                          value=0, command=self.gp.grand)

        self.cs = Caesar(self.parent)
        self.cs.set_cipher_window(self)
        self.radio_button_2 = Radiobutton(self.root, text="Caesar Cipher", variable=self.choise,
                                          value=1, command=self.cs.caesar)

        self.search_entry.pack()
        self.label.pack()
        self.radio_button_1.pack()
        self.radio_button_2.pack()

    def validate_text(self, event):
        pattern = re.compile('[A-Za-z \n]')
        return bool(pattern.match(event.char))

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()


class BlankTab():
    def __init__(self, parent):
        self.parent = parent
        
    def set_cipher_window(self, cipher_window):
        self.cipher_window = cipher_window
        
    def draw_tab_w_cls_btn(self, name: str):
        self.parent.tab = Frame(self.parent.tabs_control)
        self.parent.tabs_control.add(self.parent.tab, text=name)
        self.parent.tabs_control.select(self.parent.tab)
        self.parent.btn_cls = Button(self.parent.tab, width=2, height=1, relief=GROOVE, text="x",
                                     command=lambda: self.parent.tabs_control.forget(self.parent.tabs_control.select()))
        self.parent.btn_cls.pack(anchor='ne')


class GrandPrix():
    def __init__(self, parent):
        self.parent = parent
        self.vars = Vars()
        self.btab = BlankTab(parent)

    def set_cipher_window(self, cipher_window):
        self.btab.set_cipher_window(cipher_window)

    def grand(self):
        self.btab.draw_tab_w_cls_btn(name="grand")

        self.parent.label_1 = Label(self.parent.tab, text="Number of words:")
        self.parent.entry_1 = Entry(self.parent.tab)
        self.parent.label_2 = Label(self.parent.tab, text="List of words (Enter is separator):")
        self.parent.text_1 = Text(self.parent.tab, width=30, height=10)  # this widget needs to validate input
        self.parent.button_1 = Button(self.parent.tab, text="Input", command=self.check_size)
        self.parent.label_3 = Label(self.parent.tab, text="Plain text:")
        self.parent.sctxt_1 = ScrolledText(self.parent.tab, width=30, height=10)
        self.parent.button_2 = Button(self.parent.tab, text="Encode", command=self.encode)
        self.parent.label_4 = Label(self.parent.tab, text="Cipher text:")
        self.parent.sctxt_2 = ScrolledText(self.parent.tab, width=30, height=10)

        self.parent.label_1.pack()
        self.parent.entry_1.pack()

        self.parent.entry_1.configure(validate="key", validatecommand=(self.parent.register(self.validate_entry), "%P"))
        self.parent.entry_1.bind('<Return>', self.check_number)

        self.btab.cipher_window.root.destroy()

    def validate_entry(self, P):
        pattern = re.compile('[0-9]+')
        return bool(pattern.match(P))

    def check_number(self, event):
        number = self.parent.entry_1.get()
        if int(number) > 36 or int(number) < 2:
            showerror("Warning!", "The number of words should be no more than 36 and no less than 2. Try again")
        else:
            self.parent.entry_1.configure(state="disabled")
            self.parent.label_2.pack()
            self.parent.text_1.pack()
            self.parent.button_1.pack()

    def check_size(self):
        words = self.parent.text_1.get("1.0", "end-1c").upper().split()
        num = int(self.parent.entry_1.get())
        access = False
        for word in words:
            if num == len(word):
                self.parent.text_1.configure(state="disabled")
                self.parent.button_1.configure(state="disabled")
                access = True
            else:
                showerror("Warning!", f'The number of letters in the word must be exactly {num}. Try again')
                self.parent.text_1.configure(state="normal")
                self.parent.button_1.configure(state="normal")
                access = False
                break
        if num != len(words):
            showerror("Warning!", f'The number words must be exactly {num}. Try again')
            self.parent.text_1.configure(state="normal")
            self.parent.button_1.configure(state="normal")
            access = False
        if access:
            self.parent.label_3.pack()
            self.parent.sctxt_1.pack()
            self.parent.button_2.pack()
            self.parent.label_4.pack()
            self.parent.sctxt_2.pack()
            self.create_dict(words, num)

    def create_dict(self, w: list, n: int):
        for i in range(n):
            for j in range(n):
                self.vars.dict[str(w[i][j])].append(str(self.vars.base[i % n]) + str(self.vars.base[j % n]))

    def encode(self):
        txt = re.sub(r'[^A-Z]', '', self.parent.sctxt_1.get("1.0", "end-1c").upper())

        for i in range(len(txt)):
            try:
                self.vars.cipher += random.choice(self.vars.dict[txt[i]])
                if (i + 1) % 16 == 0:
                    self.vars.cipher += '\n'
                else:
                    self.vars.cipher += '\t'
            except:
                showerror("Warning!", f'Letter {txt[i]} is not in the dictionary. Try again')
                self.vars.cipher = ''
                break

        self.parent.sctxt_2.insert(INSERT, self.vars.cipher)


class Caesar():
    def __init__(self, parent):
        self.parent = parent
        self.btab = BlankTab(parent)

    def set_cipher_window(self, cipher_window):
        self.btab.set_cipher_window(cipher_window)

    def caesar(self):
        self.btab.draw_tab_w_cls_btn(name="caesar")

        self.parent.label_1 = Label(self.parent.tab, text="Shift:")
        self.parent.entry_1 = Entry(self.parent.tab)
        self.parent.label_2 = Label(self.parent.tab, text="Plaintext:")

        self.parent.label_1.pack()
        self.parent.entry_1.pack()
        self.parent.label_2.pack()

        self.btab.cipher_window.root.destroy()
