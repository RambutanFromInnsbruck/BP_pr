import re
import random
from tkinter import *
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText
from tab_templates import BlankTab
from window_templates import DialogueWindow
from variables import *
from custom_widgets import ToggleButton


class GrandPrixEnc():
    def __init__(self, parent):
        self.parent = parent
        self.vars = Vars()
        self.btab = BlankTab(parent)

    def set_cipher_window(self, cypher_window):
        self.btab.set_riddle_window(cypher_window)

    def execute(self):
        self.btab.draw_tab_w_cls_btn("grand_enc")

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

        self.label_gp_nmbr.place(x=200, y=27)
        self.entry_gp_nmbr.place(x=190, y=50)

        self.entry_gp_nmbr.bind("<KeyPress>", lambda e: self.btab.validate(e, r'[0-9]+'))
        self.entry_gp_nmbr.bind('<Return>', self.check_number)
        self.text_gp_dict.bind("<KeyPress>", lambda e: self.btab.validate(e, r'[a-zA-Z \n]'))
        self.sctxt_gp_pln.bind("<KeyPress>", lambda e: self.btab.validate(e, r'[a-zA-Z \n]'))

        self.btab.riddle_window.root.destroy()

    def check_number(self, *event):
        number = self.entry_gp_nmbr.get()
        if number == '':
            showerror("Warning!", "Enter a non-empty value")
        elif int(number) > 36 or int(number) < 2:
            showerror("Warning!", "The number of words should be no more than 36 and no less than 2. Try again")
        else:
            self.entry_gp_nmbr.configure(state="disabled")
            self.label_gp_dict.place(x=335, y=27)
            self.text_gp_dict.place(x=330, y=50)
            self.button_gp_dict.place(x=430, y=220)

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
            self.label_gp_pln.place(x=170, y=250)
            self.sctxt_gp_pln.place(x=75, y=273)
            self.button_gp_enc.place(x=310, y=443)
            self.label_gp_enc.place(x=440, y=250)
            self.sctxt_gp_enc.place(x=350, y=273)
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
                self.vars.result += random.choice(self.vars.dict[txt[i]])
                if (i + 1) % 16 == 0:
                    self.vars.result += '\n'
                else:
                    self.vars.result += '\t'
            except:
                showerror("Warning!", f'Letter {txt[i]} is not in the dictionary. Try again')
                self.vars.result = ''
                break

        self.sctxt_gp_enc.insert(INSERT, self.vars.result)
        self.vars.result = ''


class CaesarEnc():
    def __init__(self, parent):
        self.parent = parent
        self.vars = Vars()
        self.btab = BlankTab(parent)

    def set_cipher_window(self, cipher_window):
        self.btab.set_riddle_window(cipher_window)

    def execute(self):
        self.btab.draw_tab_w_cls_btn("caesar_enc")

        self.label_cs_shft = Label(self.btab.tab_frame, text="Shift:")
        self.entry_cs_shft = Entry(self.btab.tab_frame)
        self.toggle_btn = ToggleButton(self.btab.tab_frame, width=40, height=25)
        self.toggle_label = Label(self.btab.tab_frame, text="Alphabet")
        self.label_cs_pln = Label(self.btab.tab_frame, text="Plaintext:")
        self.sctxt_cs_pln = ScrolledText(self.btab.tab_frame, width=30, height=10)
        self.button_cs_enc = Button(self.btab.tab_frame, text="Encode", command=self.encode_caesar)
        self.label_cs_enc = Label(self.btab.tab_frame, text="Cipher text:")
        self.sctxt_cs_enc = ScrolledText(self.btab.tab_frame, width=30, height=10)

        self.label_cs_shft.place(x=295, y=27)
        self.entry_cs_shft.place(x=250, y=50)

        self.toggle_btn.set_command(self.on_toggle)

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
            self.toggle_btn.place(x=420, y=47)
            self.toggle_label.place(x=465, y=48)
            self.label_cs_pln.place(x=170, y=100)
            self.sctxt_cs_pln.place(x=75, y=123)
            self.button_cs_enc.place(x=310, y=293)
            self.label_cs_enc.place(x=440, y=100)
            self.sctxt_cs_enc.place(x=350, y=123)

    def on_toggle(self):
        self.state = "ASCII" if self.toggle_btn.get_state() else "Alphabet"
        self.toggle_label.config(text=f"{self.state}")

    def encode_caesar(self):
        self.sctxt_cs_enc.delete("1.0", "end")
        txt = self.sctxt_cs_pln.get("1.0", "end-1c")
        shift = int(self.entry_cs_shft.get())

        if self.toggle_btn.get_state():  # ASCII
            for char in txt:
                if START_CHAR_ASCII <= ord(char) <= LAST_CHAR_ASCII:
                    self.vars.result += chr(
                        ((ord(char) + shift - START_CHAR_ASCII) % QUANTITY_ASCII) + START_CHAR_ASCII)
                else:
                    self.vars.result += char
        else: # Alphabet
            for char in txt:
                if char.isupper():
                    self.vars.result += chr(
                        ((ord(char) + shift - START_CHAR_ALPH_CAP) % QUANTITY_ALPH_CAP) + START_CHAR_ALPH_CAP)
                elif char.islower():
                    self.vars.result += chr(
                        ((ord(char) + shift - START_CHAR_ALPH_SMALL) % QUANTITY_ALPH_SMALL) + START_CHAR_ALPH_SMALL)
                else:
                    self.vars.result += char

        self.sctxt_cs_enc.insert(INSERT, self.vars.result)
        self.vars.result = ''

class EncodeCipherWindow(DialogueWindow):

    CIPHER_TYPES = [
        (GrandPrixEnc, "Grand Prix Cipher"),
        (CaesarEnc, "Caesar Cipher")
    ]

    def __init__(self, parent):
        super().__init__(parent, "Encode Dialogue")
