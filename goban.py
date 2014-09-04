"""
The code to represent the Goban and the stones placed on it.
Along with the functionality associated with "whole-board" issues.
Eg: Anything that requires knowledge of the board size or the stones on
it will likely be handled in this class
"""

from stone import *
from group import *

class BoardError(Exception):
    """Empty class to simply rename the basic Exception"""
    pass


class Goban(object):
    def __init__(self, size):
        if size % 2 == 0:
            raise BoardError("Board sizes must be odd numbers")
        elif size > 35:
            raise BoardError("Board sizes greater than 35 are not supported")
        else:
            vals = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            self.base_values = list(vals[:size])
            self.size = size
            self.board = [None for _ in range(size * size)]
            self.groups = []

    def get(self, index):
        return self.board[index]

    def __str__(self):
        s = "  "
        for i in range(self.size):
            s += "{0} ".format(self.base_values[i])
        for i in range(len(self.board)):
            if i % self.size == 0:
                s += "\n"
                s += "{} ".format(self.base_values[i // self.size])
            v = self.board[i]
            if v is None:
                s += ". "
            else:
                s += "{} ".format(v)
        s += "\n"
        return s

    def position_tuple_for_index(self, index):
        x = self.base_values[index % self.size]
        y = self.base_values[index // self.size]
        return x, y

    def index_from_position_tuple(self, position):
        x = self.base_values.index(position[0])
        y = self.base_values.index(position[1])
        return y * self.size + x

    def place_stone(self, stone_color, position):
        index = self.index_from_position_tuple(position)
        stone = Stone(stone_color)
        self.board[index] = stone

    def north_index(self, index):
        return index - self.size

    def east_index(self, index):
        return index + 1

    def south_index(self, index):
        return index + self.size

    def west_index(self, index):
        return index - 1