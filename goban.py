from stone import *
from group import *

class BoardError(Exception):
    """Empty class to simply rename the basic Exception"""
    pass


class Goban(object):
    """
    The code to represent the Goban and the stones placed on it.
    Along with the functionality associated with "whole-board" issues.
    Eg: Anything that requires knowledge of the board size or the stones on
    it will likely be handled in this class
    """

    def __init__(self, size):
        """
        Initializes a board object
        :param size: The size of the board, must be odd and less than 35
        :return: Returns the initialized board
        """
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
        """
        Gets the item on the board at the given index
        :param index: The integer index of the position, to convert to an integer
                      index from a positional tuple, use the index_from_position_tuple method
        :return: Returns the item at the index, this will either be None, or a Stone object
        """
        return self.board[index]

    def __str__(self):
        """
        :return: The board represented as a string: empty vertices are denoted with a dot
                 white stones with *, and black stones with o. Coordinate numbers are
                 marked along all sides
        """
        s = "\n  "
        for i in range(self.size):
            s += "{0} ".format(self.base_values[i])
        for i in range(len(self.board)):
            if i % self.size == 0:
                s += "\n{0} ".format(self.base_values[i // self.size])
            v = self.board[i]
            if v is None:
                s += ". "
            else:
                s += "{} ".format(v)
            if i % self.size == self.size - 1:
                s += "{0}".format(self.base_values[i // self.size])
        s += "\n  "
        for i in range(self.size):
            s += "{0} ".format(self.base_values[i])
        s += "\n"
        return s

    def position_tuple_for_index(self, index):
        """
        Converts an integer index into the corresponding position tuple
        :param index: A single integer within the range of the self.board list
        :return: A tuple of two strings with the X and Y coordinates of the position, respectively
        """
        x = self.base_values[index % self.size]
        y = self.base_values[index // self.size]
        return x, y

    def index_from_position_tuple(self, position):
        """
        Translates a positional tuple into an integer index.
        :param position: Either a tuple of strings, or a string containing the X and Y
                         coordinates of the move, in that order
        :return: Returns the index for self.board that corresponds with the given position
        """
        x = self.base_values.index(position[0])
        y = self.base_values.index(position[1])
        return y * self.size + x

    def valid_move(self, stone_color, index):
        """
        Tests whether a given move is valid
        :param stone_color: A member of the StoneColor enum
        :param index: The integer index of the intended stone placement
        :return: True if the move is valid, false otherwise
        """
        if self.get(index) is None:
            return True
        else:
            return False

    def place_stone(self, stone_color, position):
        """
        Places a stone of the given color at the position indicated by the positional tuple
        :param stone_color: A member of the StoneColor enum (StoneColor.black or StoneColor.white)
        :param position: A tuple of the X and Y coordinates for the move
        :return: Returns True if the move was successful, False otherwise
        """
        index = self.index_from_position_tuple(position)
        if self.valid_move(stone_color, index):
            stone = Stone(stone_color)
            self.board[index] = stone
            return True
        else:
            return False

    def white_play_at(self, position):
        self.place_stone(StoneColor.white, position)

    def black_play_at(self, position):
        self.place_stone(StoneColor.black, position)

    def north_index(self, index):
        """
        Gets the index of the stone directly to the "north" of the current stone
        :param index: The integer index of the current stone
        :return: The integer index of the northern stone
        """
        return index - self.size

    def east_index(self, index):
        """
        Gets the index of the stone directly to the "east" of the current stone
        :param index: The integer index of the current stone
        :return: The integer index of the eastern stone
        """
        return index + 1

    def south_index(self, index):
        """
        Gets the index of the stone directly to the "south" of the current stone
        :param index: The integer index of the current stone
        :return: The integer index of the southern stone
        """
        return index + self.size

    def west_index(self, index):
        """
        Gets the index of the stone directly to the "west" of the current stone
        :param index: The integer index of the current stone
        :return: The integer index of the western stone
        """
        return index - 1

    def cardinal_stones(self, index):
        """
        Gets the stones directly above, below, and to the sides of the stone at the index
        :param index: The index of the original stone as an int (not a positional tuple)
        :return: Returns a list of the contents of the vertices directly adjacent, which
                 may or may not contain stones
        """
        return [
            self.get(self.north_index(index)),
            self.get(self.east_index(index)),
            self.get(self.south_index(index)),
            self.get(self.west_index(index))
        ]