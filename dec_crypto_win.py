from tkinter import *
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText
import re
from tab_templates import BlankTab
from window_templates import DialogueWindow
from variables import *


class GrandPrixDec():
    def __init__(self, parent):
        self.parent = parent
        self.vars = Vars()
        self.btab = BlankTab(parent)

    def set_cipher_window(self, cipher_window):
        self.btab.set_riddle_window(cipher_window)

    def execute(self):
        self.btab.draw_tab_w_cls_btn("grand_dec")

        self.label_gp_nmbr = Label(self.btab.tab_frame, text="Number of words:")
        self.entry_gp_nmbr = Entry(self.btab.tab_frame)
        self.label_gp_dict = Label(self.btab.tab_frame, text="List of words (Enter & space are separators):")
        self.text_gp_dict = Text(self.btab.tab_frame, width=30, height=10)
        self.button_gp_dict = Button(self.btab.tab_frame, text="Input", command=self.check_size)
        self.label_gp_enc = Label(self.btab.tab_frame, text="Cipher text (Enter & space are separators):")
        self.sctxt_gp_enc = ScrolledText(self.btab.tab_frame, width=30, height=10)
        self.button_gp_dec = Button(self.btab.tab_frame, text="Decode", command=self.decode_grand)
        self.label_gp_pln = Label(self.btab.tab_frame, text="Plain text:")
        self.sctxt_gp_pln = ScrolledText(self.btab.tab_frame, width=30, height=10)

        self.label_gp_nmbr.pack()
        self.entry_gp_nmbr.pack()

        self.entry_gp_nmbr.bind("<KeyPress>", lambda e: self.btab.validate(e, r'[0-9]+'))
        self.entry_gp_nmbr.bind('<Return>', self.check_number)
        self.text_gp_dict.bind("<KeyPress>", lambda e: self.btab.validate(e, r'[a-zA-Z \n]'))

        self.btab.riddle_window.root.destroy()

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
            self.label_gp_enc.pack()
            self.sctxt_gp_enc.pack()
            self.button_gp_dec.pack()
            self.label_gp_pln.pack()
            self.sctxt_gp_pln.pack()
            self.create_dict(words, num)

    def create_dict(self, w: list, n: int):
        for i in range(n):
            for j in range(n):
                self.vars.dict[str(w[i][j])].append(str(BASE[i % n]) + str(BASE[j % n]))

    def decode_grand(self):
        self.sctxt_gp_pln.delete("1.0", "end")
        txt = re.sub(r'[^a-z0-9 \n\t]', '', self.sctxt_gp_enc.get("1.0", "end-1c").lower())

        parts = txt.split()
        rev_dict = {}
        result = []

        for key, values in self.vars.dict.items():
            for value in values:
                if value not in rev_dict:
                    rev_dict[value] = key

        for part in parts:
            try:
                result.append(rev_dict[part])
            except:
                showerror("Warning!", f'Address {part} is not in the dictionary. Try again')
                result = []
                break

        self.vars.result = self.vars.result.join(result)
        self.sctxt_gp_pln.insert(INSERT, self.vars.result)
        self.vars.result = ''


class CaesarDec():
    def __init__(self, parent):
        self.parent = parent
        self.vars = Vars()
        self.btab = BlankTab(parent)

    def set_cipher_window(self, cipher_window):
        self.btab.set_riddle_window(cipher_window)

    def execute(self):
        self.btab.draw_tab_w_cls_btn("caesar_dec")

        self.label_cs_shft = Label(self.btab.tab_frame, text="Shift:")
        self.entry_cs_shft = Entry(self.btab.tab_frame)
        self.label_cs_enc = Label(self.btab.tab_frame, text="Cipher text:")
        self.sctxt_cs_enc = ScrolledText(self.btab.tab_frame, width=30, height=10)
        self.button_cs_dec = Button(self.btab.tab_frame, text="Decode", command=self.decode_caesar)
        self.label_cs_pln = Label(self.btab.tab_frame, text="Plaintext:")
        self.sctxt_cs_pln = ScrolledText(self.btab.tab_frame, width=30, height=10)

        self.label_cs_shft.pack()
        self.entry_cs_shft.pack()

        self.entry_cs_shft.bind("<KeyPress>", lambda e: self.btab.validate(e, r'[0-9]+'))
        self.entry_cs_shft.bind('<Return>', self.check_shift)

        self.btab.riddle_window.root.destroy()

    def check_shift(self, *event):
        number = self.entry_cs_shft.get()
        if number == '':
            showerror("Warning!", "Enter a non-empty value")
        elif int(number) < 1:
            showerror("Warning!", "Shift should be at least 1. Try again")
        else:
            self.entry_cs_shft.configure(state="disabled")
            self.label_cs_enc.pack()
            self.sctxt_cs_enc.pack()
            self.button_cs_dec.pack()
            self.label_cs_pln.pack()
            self.sctxt_cs_pln.pack()

    def decode_caesar(self):
        self.sctxt_cs_pln.delete("1.0", "end")
        txt = self.sctxt_cs_enc.get("1.0", "end-1c")
        shift = int(self.entry_cs_shft.get())

        for char in txt:
            self.vars.result += chr(((ord(char) - shift - START_CHAR) % QUANTITY) + START_CHAR)

        self.sctxt_cs_pln.insert(INSERT, self.vars.result)
        self.vars.result = ''


class DecodeCipherWindow(DialogueWindow):
    CIPHER_TYPES = [
        (GrandPrixDec, "Grand Prix Cipher"),
        (CaesarDec, "Caesar Cipher")
    ]

    def __init__(self, parent):
        super().__init__(parent, "Decode Dialogue")
