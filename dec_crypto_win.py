from tkinter import *
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText
import re
from tab_templates import BlankTab
from window_templates import DialogueWindow
from variables import *
from custom_widgets import ToggleButton


class GrandPrixDec(BlankTab):
    def __init__(self, parent):
        super().__init__(parent)
        self.vars = Vars()

    def execute(self):
        self.draw_tab_w_cls_btn("grand_dec")

        self.label_gp_nmbr = Label(self.tab_frame, text="Number of words:")
        self.entry_gp_nmbr = Entry(self.tab_frame)
        self.label_gp_dict = Label(self.tab_frame, text="List of words (Enter & space are separators):")
        self.text_gp_dict = Text(self.tab_frame, width=30, height=10)
        self.button_gp_dict = Button(self.tab_frame, text="Input", command=self.check_size)
        self.label_gp_enc = Label(self.tab_frame, text="Cipher text (Enter & space are separators):")
        self.sctxt_gp_enc = ScrolledText(self.tab_frame, width=30, height=10)
        self.button_gp_dec = Button(self.tab_frame, text="Decode", command=self.decode_grand)
        self.label_gp_pln = Label(self.tab_frame, text="Plain text:")
        self.sctxt_gp_pln = ScrolledText(self.tab_frame, width=30, height=10)

        self.label_gp_nmbr.place(x=200, y=27)
        self.entry_gp_nmbr.place(x=190, y=50)
        self.label_gp_dict.place(x=335, y=27)
        self.text_gp_dict.place(x=330, y=50)
        self.button_gp_dict.place(x=430, y=220)
        self.label_gp_enc.place(x=82, y=250)
        self.sctxt_gp_enc.place(x=75, y=273)
        self.button_gp_dec.place(x=310, y=443)
        self.label_gp_pln.place(x=445, y=250)
        self.sctxt_gp_pln.place(x=350, y=273)

        self.entry_gp_nmbr.bind("<KeyPress>", lambda e: self.validate(e, r'[0-9]+'))
        self.entry_gp_nmbr.bind('<Return>', self.check_number)
        self.text_gp_dict.bind("<KeyPress>", lambda e: self.validate(e, r'[a-zA-Z \n\t]'))
        self.sctxt_gp_enc.bind("<KeyPress>", lambda e: self.validate(e, r'[a-z0-9 \n\t]'))

        self.button_gp_dict.configure(state="disabled")
        self.button_gp_dec.configure(state="disabled")
        self.sctxt_gp_pln.configure(state="disabled")

        self.riddle_window.root.destroy()

    def check_number(self, *event):
        number = self.entry_gp_nmbr.get()
        if number == '':
            showerror("Warning!", "Enter a non-empty value")
        elif int(number) > 36 or int(number) < 2:
            showerror("Warning!", "The number of words should be no more than 36 and no less than 2. Try again")
        else:
            self.entry_gp_nmbr.configure(state="disabled")
            self.button_gp_dict.configure(state="normal")

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
            self.vars.dict = {key: [] for key in self.vars.dict}
            self.create_dict(words, num)
            self.button_gp_dec.configure(state="normal")

    def create_dict(self, w: list, n: int):
        for i in range(n):
            for j in range(n):
                self.vars.dict[str(w[i][j])].append(str(BASE[i % n]) + str(BASE[j % n]))

    def decode_grand(self):
        self.sctxt_gp_pln.configure(state="normal")
        self.sctxt_gp_pln.delete("1.0", "end")
        txt = self.sctxt_gp_enc.get("1.0", "end-1c")

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
        self.sctxt_gp_pln.configure(state="disabled")

    def rerun(self):
        self.entry_gp_nmbr.configure(state="normal")
        self.text_gp_dict.configure(state="normal")
        self.sctxt_gp_pln.configure(state="normal")

        self.entry_gp_nmbr.delete(0, "end")
        self.text_gp_dict.delete("1.0", "end")
        self.sctxt_gp_enc.delete("1.0", "end")
        self.sctxt_gp_pln.delete("1.0", "end")

        self.button_gp_dict.configure(state="disabled")
        self.button_gp_dec.configure(state="disabled")
        self.sctxt_gp_pln.configure(state="disabled")

    def undo(self):
        if self.entry_gp_nmbr['state'] == "normal":
            self.rerun()
        if self.button_gp_dict['state'] == "normal":
            self.button_gp_dict.configure(state="disabled")
            self.entry_gp_nmbr.configure(state="normal")
        if self.button_gp_dec['state'] == "normal":
            self.button_gp_dec.configure(state="disabled")
            self.text_gp_dict.configure(state="normal")
            self.button_gp_dict.configure(state="normal")
            self.sctxt_gp_pln.configure(state="normal")
            self.sctxt_gp_pln.delete("1.0", "end")
            self.sctxt_gp_pln.configure(state="disabled")


class CaesarDec(BlankTab):
    def __init__(self, parent):
        super().__init__(parent)
        self.vars = Vars()

    def execute(self):
        self.draw_tab_w_cls_btn("caesar_dec")

        self.label_cs_shft = Label(self.tab_frame, text="Shift:")
        self.entry_cs_shft = Entry(self.tab_frame)
        self.toggle_btn = ToggleButton(self.tab_frame, width=40, height=25)
        self.toggle_label = Label(self.tab_frame, text="Alphabet")
        self.label_cs_enc = Label(self.tab_frame, text="Cipher text:")
        self.sctxt_cs_enc = ScrolledText(self.tab_frame, width=30, height=10)
        self.button_cs_dec = Button(self.tab_frame, text="Decode", command=self.decode_caesar)
        self.button_cs_brtfrc = Button(self.tab_frame, text="Bruteforce", command=self.bruteforce_caesar)
        self.label_cs_pln = Label(self.tab_frame, text="Plaintext:")
        self.sctxt_cs_pln = ScrolledText(self.tab_frame, width=30, height=10)

        self.label_cs_shft.place(x=295, y=27)
        self.entry_cs_shft.place(x=250, y=50)
        self.toggle_btn.place(x=420, y=47)
        self.toggle_label.place(x=465, y=48)
        self.label_cs_enc.place(x=165, y=100)
        self.sctxt_cs_enc.place(x=75, y=123)
        self.button_cs_dec.place(x=310, y=293)
        self.button_cs_brtfrc.place(x=302, y=323)
        self.label_cs_pln.place(x=445, y=100)
        self.sctxt_cs_pln.place(x=350, y=123)

        self.toggle_btn.set_command(self.on_toggle)

        self.entry_cs_shft.bind("<KeyPress>", lambda e: self.validate(e, r'[0-9]+'))
        self.entry_cs_shft.bind('<Return>', self.check_shift)
        self.sctxt_cs_enc.bind("<KeyPress>", lambda e: self.validate(e, r'[!-~ \n\t]'))

        self.button_cs_dec.configure(state="disabled")
        self.sctxt_cs_pln.configure(state="disabled")

        self.riddle_window.root.destroy()

    def check_shift(self, *event):
        number = self.entry_cs_shft.get()
        if number == '':
            showerror("Warning!", "Enter a non-empty value")
        elif int(number) < 1:
            showerror("Warning!", "Shift should be at least 1. Try again")
        else:
            self.entry_cs_shft.configure(state="disabled")
            self.button_cs_dec.configure(state="normal")
            self.button_cs_brtfrc.configure(state="disabled")

    def on_toggle(self):
        self.state = "ASCII" if self.toggle_btn.get_state() else "Alphabet"
        self.toggle_label.config(text=f"{self.state}")

    def _cs_decrypt(self, txt: str, shift: int):
        self.vars.result = ''
        if self.toggle_btn.get_state():  # ASCII
            for char in txt:
                if START_CHAR_ASCII <= ord(char) <= LAST_CHAR_ASCII:
                    self.vars.result += chr(
                        ((ord(char) - shift - START_CHAR_ASCII) % QUANTITY_ASCII) + START_CHAR_ASCII)
                else:
                    self.vars.result += char
        else: # Alphabet
            for char in txt:
                if char.isupper():
                    self.vars.result += chr(
                        ((ord(char) - shift - START_CHAR_ALPH_CAP) % QUANTITY_ALPH_CAP) + START_CHAR_ALPH_CAP)
                elif char.islower():
                    self.vars.result += chr(
                        ((ord(char) - shift - START_CHAR_ALPH_SMALL) % QUANTITY_ALPH_SMALL) + START_CHAR_ALPH_SMALL)
                else:
                    self.vars.result += char
        return self.vars.result

    def _cs_analyze(self, txt: str):
        capital_txt = txt.upper()
        words = capital_txt.split()

        # Counting the most common words
        common_word_count = 0
        for word in words:
            clean_word = re.sub(r'[^A-Z]', '', word)
            if clean_word in self.vars.common_words:
                common_word_count += 1

        # Checking for the presence of vowels
        vowel_count = 0
        letter_count = 0
        for char in capital_txt:
            if char.isalpha():
                letter_count += 1
                if char in VOWEL_LETTERS:
                    vowel_count += 1
        vowel_ratio = vowel_count / letter_count if letter_count > 0 else 0

        # Frequency analysis
        freq_score = 0
        if letter_count > 0:
            freq_dict = {}
            for char in capital_txt:
                if char.isalpha():
                    freq_dict[char] = freq_dict.get(char, 0) + 1
            for char in freq_dict:
                observed_freq = freq_dict[char] / letter_count * 100
                expected_freq = self.vars.english_freq[char]
                freq_score += (observed_freq - expected_freq) ** 2

        # Checking for unusual letter combinations
        unusual_combinations = 0
        for i in range(len(capital_txt) - 1):
            if capital_txt[i].isalpha() and capital_txt[i + 1].isalpha():
                bigram = capital_txt[i:i + 2]
                if bigram in self.vars.rare_bigram:
                    unusual_combinations += 1

        # Combined assessment with different weights
        total_score = (
                -common_word_count * COMMON_WORD_COEFFICIENT +
                freq_score * FREQ_COEFFICIENT +
                abs(vowel_ratio - EXPECTED_VOWEL_RATIO) * VOWEL_COEFFICIENT +
                unusual_combinations * UNUSUAL_BIGRAM_COEFFICIENT
        )

        return total_score

    def decode_caesar(self):
        self.sctxt_cs_pln.configure(state="normal")
        self.sctxt_cs_pln.delete("1.0", "end")
        txt = self.sctxt_cs_enc.get("1.0", "end-1c")
        shift = int(self.entry_cs_shft.get())
        plane_text = self._cs_decrypt(txt, shift)
        self.sctxt_cs_pln.insert(INSERT, plane_text)
        self.entry_cs_shft.configure(state="disabled")

    def bruteforce_caesar(self):
        self.entry_cs_shft.delete(0, "end")
        self.entry_cs_shft.configure(state="disabled")
        self.sctxt_cs_pln.configure(state="normal")
        self.sctxt_cs_pln.delete("1.0", "end")
        txt = self.sctxt_cs_enc.get("1.0", "end-1c")

        if txt == '':
            self.sctxt_cs_pln.configure(state="disabled")

        if self.toggle_btn.get_state():  # ASCII
            max_shift = QUANTITY_ASCII
        else: # Alphabet
            max_shift = QUANTITY_ALPH_SMALL

        results = []
        for shift in range(1, max_shift):
            plane_text = self._cs_decrypt(txt, shift)
            score = self._cs_analyze(plane_text)
            results.append((shift, score, plane_text))

        if self.toggle_btn.get_state() == False: # Alphabet
            results.sort(key=lambda x: x[1])

        for shift, score, plane_text in results:
            self.sctxt_cs_pln.insert(INSERT, f'Possible shift: {shift}\n\n')
            self.sctxt_cs_pln.insert(INSERT, f'{plane_text}\n\n')

        self.sctxt_cs_pln.configure(state="disabled")

    def rerun(self):
        self.entry_cs_shft.configure(state="normal")
        self.sctxt_cs_pln.configure(state="normal")
        self.button_cs_brtfrc.configure(state="normal")

        self.entry_cs_shft.delete(0, "end")
        self.sctxt_cs_enc.delete("1.0", "end")
        self.sctxt_cs_pln.delete("1.0", "end")

        self.button_cs_dec.configure(state="disabled")
        self.sctxt_cs_pln.configure(state="disabled")

    def undo(self):
        if self.entry_cs_shft['state'] == "normal":
            self.rerun()
        if self.button_cs_dec['state'] == "normal" or self.button_cs_brtfrc['state'] == "normal":
            self.button_cs_dec.configure(state="disabled")
            self.entry_cs_shft.configure(state="normal")
            self.button_cs_brtfrc.configure(state="normal")
            self.sctxt_cs_pln.configure(state="normal")
            self.sctxt_cs_pln.delete("1.0", "end")
            self.sctxt_cs_pln.configure(state="disabled")


class DecodeCipherWindow(DialogueWindow):
    CONCEALMENT_TYPES = [
        (GrandPrixDec, "Grand Prix Cipher"),
        (CaesarDec, "Caesar Cipher")
    ]

    def __init__(self, parent):
        super().__init__(parent, "Decode Dialogue")
