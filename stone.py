from enum import Enum

class StoneColor(Enum):
    """ Enumerates the available colors """
    black = 0
    white = 1


class Stone(object):
    """
    A lightweight class to represent an individual stone
    """
    def __init__(self, color):
        self.color = color
        self.group = None

    def __str__(self):
        if self.color is not None:
            if self.color == StoneColor.white:
                return "*"
            else:
                return "o"