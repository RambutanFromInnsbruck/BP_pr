START_CHAR = ord("!")
LAST_CHAR = ord("~")
QUANTITY = LAST_CHAR - START_CHAR + 1

class Vars:
    def __init__(self):
        self.base = '0123456789abcdefghijklmnopqrstuvwxyz'
        self.cipher = ''
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
