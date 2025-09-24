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

VOWEL_LETTERS = 'AEIOUY'

class Vars:
    def __init__(self):
        self.result = ''
        self.dict = {
            'A': [], 'B': [], 'C': [], 'D': [], 'E': [],
            'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
            'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
            'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
            'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []
        }
        self.common_words = {
            'THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'I',
            'IT', 'FOR', 'NOT', 'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT',
            'THIS', 'BUT', 'HIS', 'BY', 'FROM', 'THEY', 'WE', 'SAY', 'HER', 'SHE',
            'OR', 'AN', 'WILL', 'MY', 'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR', 'WHAT',
            'SO', 'UP', 'OUT', 'IF', 'ABOUT', 'WHO', 'GET', 'WHICH', 'GO', 'ME'
        }
        self.english_freq = {
            'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
            'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
            'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
            'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
            'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
        }
        self.rare_bigram = {'ZX', 'QJ', 'ZJ', 'ZQ', 'JX', 'JQ', 'VQ', 'VZ'}