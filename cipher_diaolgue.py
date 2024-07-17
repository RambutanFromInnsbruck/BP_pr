from tkinter import *
from tkinter.ttk import Notebook
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText
import re
import random
from variables import Vars


class CipherWindow(Vars):
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
        self.radio_button_1 = Radiobutton(self.root, text="Grand Prix Cipher", variable=self.choise, value=0, command=self.grand)
        self.radio_button_2 = Radiobutton(self.root, text="Caesar Cipher", variable=self.choise, value=1, command=self.caesar)

        self.search_entry.pack()
        self.label.pack()
        self.radio_button_1.pack()
        self.radio_button_2.pack()

    # Grand Prix
    def grand(self):
        self.draw_tab_w_btn(name="grand")

        self.parent.label_1 = Label(self.parent.tab, text="Number of words:")
        self.parent.entry_1 = Entry(self.parent.tab)
        self.parent.label_2 = Label(self.parent.tab, text="List of words (Enter is separator):")
        self.parent.text_1 = Text(self.parent.tab, width=30, height=10) # this widget needs to validate input
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

        self.root.destroy()

    def caesar(self):
        self.draw_tab_w_btn(name="caesar")

        self.parent.label_1 = Label(self.parent.tab, text="Shift:")
        self.parent.entry_1 = Entry(self.parent.tab)
        self.parent.label_2 = Label(self.parent.tab, text="Plaintext:")

        self.parent.label_1.pack()
        self.parent.entry_1.pack()
        self.parent.label_2.pack()

        self.root.destroy()

    def draw_tab_w_btn(self, name: str):
        self.parent.tab = Frame(self.parent.tabs_control)
        self.parent.tabs_control.add(self.parent.tab, text=name)
        self.parent.tabs_control.select(self.parent.tab)
        self.parent.btn_cls = Button(self.parent.tab, width=2, height=1, relief=GROOVE, text="x",
                                     command=lambda: self.parent.tabs_control.forget(self.parent.tabs_control.select()))
        self.parent.btn_cls.pack(anchor='ne')

    # validation only numbers
    def validate_entry(self, P):
        pattern = re.compile('[0-9]+')
        return bool(pattern.match(P))

    def validate_text(self, event):
        pattern = re.compile('[A-Za-z \n]')
        return bool(pattern.match(event.char))

    def check_number(self, event):
        number = self.parent.entry_1.get()
        if int(number) > 36 or int(number) < 2:
            showerror("Warning!", "The number of words should be no more than 36 and no less than 2. Try again")
        else:
            self.parent.entry_1.configure(state="disabled")
            self.parent.label_2.pack()
            self.parent.text_1.pack()
            self.parent.button_1.pack()
            # self.parent.text_1.configure(validate="key",validatecommand=(self.parent.register(self.validate_text), "%S"))

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

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()
