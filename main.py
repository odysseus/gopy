"""
Programming the game of Go in Python. The current goal is a program that allows you to
play the game and understands the rules of capturing, and possibly scoring. AI is not
currently envisioned as a feature.
"""
from goban import *


if __name__ == "__main__":
    size = 9
    b = Goban(size)
    b.place_stone(StoneColor.black, ('1', '1'))
    b.place_stone(StoneColor.white, ('2', '2'))

    print(b)
