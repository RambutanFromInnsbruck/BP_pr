from tkinter import *
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText
import re
import random
from variables import Vars, QUANTITY, START_CHAR, BASE


class DecodeCipherWindow():
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
        self.radio_button_gp = Radiobutton(self.root, text="Grand Prix Cipher", variable=self.choise,
                                           value=0, command=self.gp.call_grand)

        self.cs = Caesar(self.parent)
        self.cs.set_cipher_window(self)
        self.radio_button_cs = Radiobutton(self.root, text="Caesar Cipher", variable=self.choise,
                                           value=1, command=self.cs.call_caesar)

        self.search_entry.pack()
        self.label.pack()
        self.radio_button_gp.pack()
        self.radio_button_cs.pack()

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()


class BlankTab():
    def __init__(self, parent):
        self.parent = parent
        self.tab_frame = None

        if not hasattr(parent, 'tab_counters'):
            parent.tab_counters = {}

    def set_cipher_window(self, cipher_window):
        self.cipher_window = cipher_window

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


class GrandPrix():
    def __init__(self, parent):
        self.parent = parent
        self.vars = Vars()
        self.btab = BlankTab(parent)

    def set_cipher_window(self, cipher_window):
        self.btab.set_cipher_window(cipher_window)

    def call_grand(self):
        self.btab.draw_tab_w_cls_btn("grand_dec")

        self.label_gp_nmbr = Label(self.btab.tab_frame, text="Number of words:")
        self.entry_gp_nmbr = Entry(self.btab.tab_frame)
        self.label_gp_dict = Label(self.btab.tab_frame, text="List of words (Enter & space are separators):")
        self.text_gp_dict = Text(self.btab.tab_frame, width=30, height=10)
        self.button_gp_dict = Button(self.btab.tab_frame, text="Input", command=self.check_size)
        self.label_gp_pln = Label(self.btab.tab_frame, text="Plain text:")
        self.sctxt_gp_pln = ScrolledText(self.btab.tab_frame, width=30, height=10)
        self.button_gp_enc = Button(self.btab.tab_frame, text="Encode", command=self.encode_grand)
        self.label_gp_enc = Label(self.btab.tab_frame, text="Cipher text:")
        self.sctxt_gp_enc = ScrolledText(self.btab.tab_frame, width=30, height=10)

        self.label_gp_nmbr.pack()
        self.entry_gp_nmbr.pack()

        self.entry_gp_nmbr.bind("<KeyPress>", lambda e: self.btab.validate(e, r'[0-9]+'))
        self.entry_gp_nmbr.bind('<Return>', self.check_number)
        self.text_gp_dict.bind("<KeyPress>", lambda e: self.btab.validate(e, r'[a-zA-Z \n]'))

        self.btab.cipher_window.root.destroy()

    def check_number(self, *event):
        number = self.entry_gp_nmbr.get()
        if number == '':
            showerror("Warning!", "Enter a non-empty value")
        elif int(number) > 36 or int(number) < 2:
            showerror("Warning!", "The number of words should be no more than 36 and no less than 2. Try again")
        else:
            self.entry_gp_nmbr.configure(state="disabled")
            self.label_gp_dict.pack()
            self.text_gp_dict.pack()
            self.button_gp_dict.pack()

    def check_size(self):
        words = self.text_gp_dict.get("1.0", "end-1c").upper().split()
        num = int(self.entry_gp_nmbr.get())
        access = False
        for word in words:
            if num == len(word):
                self.text_gp_dict.configure(state="disabled")
                self.button_gp_dict.configure(state="disabled")
                access = True
            else:
                showerror("Warning!", f'The number of letters in the word must be exactly {num}. Try again')
                self.text_gp_dict.configure(state="normal")
                self.button_gp_dict.configure(state="normal")
                access = False
                break
        if num != len(words):
            showerror("Warning!", f'The number words must be exactly {num}. Try again')
            self.text_gp_dict.configure(state="normal")
            self.button_gp_dict.configure(state="normal")
            access = False
        if access:
            self.label_gp_pln.pack()
            self.sctxt_gp_pln.pack()
            self.button_gp_enc.pack()
            self.label_gp_enc.pack()
            self.sctxt_gp_enc.pack()
            self.create_dict(words, num)

    def create_dict(self, w: list, n: int):
        for i in range(n):
            for j in range(n):
                self.vars.dict[str(w[i][j])].append(str(BASE[i % n]) + str(BASE[j % n]))

    def encode_grand(self):
        self.sctxt_gp_enc.delete("1.0", "end")
        txt = re.sub(r'[^A-Z]', '', self.sctxt_gp_pln.get("1.0", "end-1c").upper())

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

        self.sctxt_gp_enc.insert(INSERT, self.vars.cipher)
        self.vars.cipher = ''


class Caesar():
    def __init__(self, parent):
        self.parent = parent
        self.vars = Vars()
        self.btab = BlankTab(parent)

    def set_cipher_window(self, cipher_window):
        self.btab.set_cipher_window(cipher_window)

    def call_caesar(self):
        self.btab.draw_tab_w_cls_btn("caesar_dec")

        self.label_cs_shft = Label(self.btab.tab_frame, text="Shift:")
        self.entry_cs_shft = Entry(self.btab.tab_frame)
        self.label_cs_pln = Label(self.btab.tab_frame, text="Cipher text:")
        self.sctxt_cs_pln = ScrolledText(self.btab.tab_frame, width=30, height=10)
        self.button_cs_enc = Button(self.btab.tab_frame, text="Decode", command=self.encode_caesar)
        self.label_cs_enc = Label(self.btab.tab_frame, text="Plaintext:")
        self.sctxt_cs_enc = ScrolledText(self.btab.tab_frame, width=30, height=10)

        self.label_cs_shft.pack()
        self.entry_cs_shft.pack()

        self.entry_cs_shft.bind("<KeyPress>", lambda e: self.btab.validate(e, r'[0-9]+'))
        self.entry_cs_shft.bind('<Return>', self.check_shift)

        self.btab.cipher_window.root.destroy()

    def check_shift(self, *event):
        number = self.entry_cs_shft.get()
        if number == '':
            showerror("Warning!", "Enter a non-empty value")
        elif int(number) < 1:
            showerror("Warning!", "Shift should be at least 1. Try again")
        else:
            self.entry_cs_shft.configure(state="disabled")
            self.label_cs_pln.pack()
            self.sctxt_cs_pln.pack()
            self.button_cs_enc.pack()
            self.label_cs_enc.pack()
            self.sctxt_cs_enc.pack()

    def encode_caesar(self):
        self.sctxt_cs_enc.delete("1.0", "end")
        txt = re.sub(r'[^a-zA-Z]', '', self.sctxt_cs_pln.get("1.0", "end-1c"))
        shift = int(self.entry_cs_shft.get())

        for char in txt:
            self.vars.cipher += chr(((ord(char) + shift - START_CHAR) % QUANTITY) + START_CHAR)

        self.sctxt_cs_enc.insert(INSERT, self.vars.cipher)
        self.vars.cipher = ''
