from goban import *

"""
Programming the game of Go in Python. The current goal is a program that allows you to
play the game and understands the rules of capturing, and possibly scoring. AI is not
currently envisioned as a feature.
"""


if __name__ == "__main__":
    size = 19
    b = Goban(size)
    b.black_play_at('F3')
    b.white_play_at('3F')
    b.black_play_at('GF')
    b.white_play_at('32')
    b.black_play_at('5G')
    b.white_play_at('2D')
    b.black_play_at('EF')
    b.white_play_at('9G')
    b.black_play_at('34')
    b.white_play_at('24')

    print(b)