from enum import Enum


class StoneColor(Enum):
    """ Enumerates the available colors """
    black = 0
    white = 1
    # Highlight is used for debugging the group logic
    highlight_black = 2
    highlight_white = 3


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
            elif self.color == StoneColor.black:
                return "o"
            elif self.color == StoneColor.highlight_black:
                return "O"
            elif self.color == StoneColor.highlight_white:
                return "@"
        else:
            return "?"