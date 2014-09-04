"""
A lightweight class to represent an individual stone
"""

from enum import Enum

class StoneColor(Enum):
    black = 0
    white = 1


class Stone(object):
    def __init__(self, color):
        self.color = color
        self.group = None

    def __str__(self):
        if self.color is not None:
            if self.color == StoneColor.white:
                return "*"
            else:
                return "o"