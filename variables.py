BASE = '0123456789abcdefghijklmnopqrstuvwxyz'

START_CHAR_ASCII = ord("!")
START_CHAR_ALPH_CAP = ord("A")
START_CHAR_ALPH_SMALL = ord("a")

LAST_CHAR_ASCII = ord("~")
LAST_CHAR_ALPH_CAP = ord("Z")
LAST_CHAR_ALPH_SMALL = ord("z")

QUANTITY_ASCII = LAST_CHAR_ASCII - START_CHAR_ASCII + 1
QUANTITY_ALPH_CAP = LAST_CHAR_ALPH_CAP - START_CHAR_ALPH_CAP + 1
QUANTITY_ALPH_SMALL = LAST_CHAR_ALPH_SMALL - START_CHAR_ALPH_SMALL + 1

class Vars:
    def __init__(self):
        self.result = ''
        self.dict = {
            'A': [],
            'B': [],
            'C': [],
            'D': [],
            'E': [],
            'F': [],
            'G': [],
            'H': [],
            'I': [],
            'J': [],
            'K': [],
            'L': [],
            'M': [],
            'N': [],
            'O': [],
            'P': [],
            'Q': [],
            'R': [],
            'S': [],
            'T': [],
            'U': [],
            'V': [],
            'W': [],
            'X': [],
            'Y': [],
            'Z': []
        }
