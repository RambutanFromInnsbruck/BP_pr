BASE = '0123456789abcdefghijklmnopqrstuvwxyz'
START_CHAR = ord("!")
LAST_CHAR = ord("~")
QUANTITY = LAST_CHAR - START_CHAR + 1

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
