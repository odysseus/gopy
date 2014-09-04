from stone import *
from group import *


class BoardError(Exception):
    """Empty class to simply rename the basic Exception"""
    pass


class Goban(object):
    """
    The code to represent the Goban and the stones placed on it.
    Along with the functionality associated with "whole-board" issues.
    Eg: Anything that requires knowledge of the board size or the
    stones on it will likely be handled in this class
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
        :param index: The integer index of the position, to convert
                      to an integer index from a positional tuple, use
                      the index_from_position_tuple method
        :return: Returns the item at the index, this will either be None,
                 or a Stone object
        """
        return self.board[index]

    def __str__(self):
        """
        :return: The board represented as a string: empty vertices are denoted
                 with a dot white stones with *, and black stones with o.
                 Coordinate numbers are marked along all sides
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
        :return: A tuple of two strings with the X and Y coordinates
                 of the position, respectively
        """
        x = self.base_values[index % self.size]
        y = self.base_values[index // self.size]
        return x, y

    def index_from_position_tuple(self, position):
        """
        Translates a positional tuple into an integer index.
        :param position: Either a tuple of strings, or a string containing
                         the X and Y coordinates of the move, in that order
        :return: Returns the index for self.board that corresponds
                 with the given position
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
        if self.get(index) is not None:
            print("Invalid move - Space it occupied")
            return False
        elif self.is_suicide(stone_color, index):
            print("Invalid move - Suicide")
            return False
        else:
            return True

    def is_suicide(self, stone_color, index):
        """
        Boolean method that checks to see if making a move would result
        in the destruction of one's own pieces
        :param stone_color: The StoneColor color of the move to be made
        :param index: The integer index of the move to be made
        :return: Returns False if the move is *not* suicide, True otherwise
        """
        cardinal_indices = self.cardinal_indices(index)
        # First check to see if there are any immediate liberties
        for ci in cardinal_indices:
            card = self.get(ci)
            if card is None:
                # There is an empty liberty so the move is not suicide
                return False
        # No liberties, so all spaces around the stone are filled
        # Two conditions will save us, an enemy group being captured,
        # or a single friendly group having more than 1 liberty.
        for ci in cardinal_indices:
            card = self.get(ci)
            # Adjacent group is friendly
            if card.color == stone_color:
                # And we are not filling its last liberty
                if self.group_liberties(ci) > 1:
                    return False
            # Adjacent group is foe
            else:
                # But we *are* filling its last liberty
                if self.group_liberties(ci) == 1:
                    return False
        # If none of the above is true, this is an invalid move
        return True

    def place_stone(self, stone_color, position):
        """
        Places a stone of the given color at the position indicated
        by the positional tuple
        :param stone_color: A member of the StoneColor enum
        :param position: A tuple of the X and Y coordinates for the move
        :return: Returns True if the move was successful, False otherwise
        """
        # Get the index from the position tuple
        index = self.index_from_position_tuple(position)
        # Check to see if the move is valid
        if self.valid_move(stone_color, index):
            # If so, initialize the stone
            stone = Stone(stone_color)
            # Add it to the board
            self.board[index] = stone
            # Create a new group for the stone
            # and link it to all contiguous groups
            self.link_stone(index)
            self.test_captures(index)
            return True
        else:
            return False

    def link_stone(self, index):
        """
        Creates a new group for a newly placed stone, and if needed
        links that to all contiguous groups of the same color
        :param index: Integer index of a newly added stone
        :return: Returns None
        """
        stone = self.get(index)
        # Create a group of a single stone first,
        # this way every stone will have a group
        group = Group(self)
        group.add_member(index)
        stone.group = group
        # Add this new group to the list of all groups
        self.groups.append(group)
        # Now check for contiguous groups
        contiguous = self.contiguous_groups(index)
        # Add the single stone group to the list
        contiguous.append(group)
        # Link all of these together
        self.link_groups(contiguous)

    def contiguous_groups(self, index):
        """
        Called on a group of a single stone, when the stone is added
        to the board,for the purpose of connecting the stones to
        the contiguous groups
        :param index: The index of the stone being tested
                      (generally the one just placed on the board)
        :return: A list containing any groups that are the same color
                 and contiguous to the stone
        """
        # A container to hold contiguous groups
        contiguous = []
        # The stone object itself
        stone = self.get(index)
        # The objects at the four vertices surrounding the stone
        cardinal_stones = [self.get(i) for i in self.cardinal_indices(index)]
        for s in cardinal_stones:
            # If it is a stone, and if the stone is the same color
            if s is not None and s.color == stone.color:
                # Add it to the list of contiguous groups
                contiguous.append(s.group)
        return contiguous

    def link_groups(self, groups):
        """
        Links groups together, but does not directly test to see
        that they are contiguous
        The smaller groups are merged into the largest one
        :param groups: a list of groups to be linked
        :return: Returns None
        """
        # Find the largest group
        max_group = groups[0]
        for group in groups:
            if group.size > max_group.size:
                max_group = group
        # Remove it from the list
        groups.remove(max_group)
        # Iterate over the smaller groups
        for group in groups:
            # Merge the sets containing the stones in that group
            max_group.add_members(group.members)
            for stone_index in group.members:
                self.get(stone_index).group = max_group
            # And remove the smaller group from the global list
            self.groups.remove(group)

    def test_captures(self, index):
        """
        Takes the index of a newly placed stone and checks to see if any of the
        surrounding groups were captured by its placement
        :param index: The index of a newly placed stone
        :return: Returns None
        """
        cardinal_indices = self.cardinal_indices(index)
        for i in cardinal_indices:
            if self.get(i) is not None:
                if self.group_captured(i):
                    self.remove_group(i)

    def white_play_at(self, position):
        """Shorthand method for playing a move as white"""
        self.place_stone(StoneColor.white, position)

    def black_play_at(self, position):
        """Shorthand method for playing a move as black"""
        self.place_stone(StoneColor.black, position)

    def north_index(self, index):
        """
        Gets the index of the stone directly to the "north"
        :param index: The integer index of the current stone
        :return: The integer index of the northern stone
        """
        return index - self.size

    def east_index(self, index):
        """
        Gets the index of the stone directly to the "east"
        :param index: The integer index of the current stone
        :return: The integer index of the eastern stone
        """
        return index + 1

    def south_index(self, index):
        """
        Gets the index of the stone directly to the "south"
        :param index: The integer index of the current stone
        :return: The integer index of the southern stone
        """
        return index + self.size

    def west_index(self, index):
        """
        Gets the index of the stone directly to the "west"
        :param index: The integer index of the current stone
        :return: The integer index of the western stone
        """
        return index - 1

    def cardinal_indices(self, index):
        """
        Returns a list of indices that are contiguous to the index provided
        :param index: Integer index
        :return: A list of indices
        """
        cards = [
            self.north_index(index),
            self.east_index(index),
            self.south_index(index),
            self.west_index(index)
        ]
        return [i for i in cards if 0 < i < (self.size * self.size)]

    def highlight_group_at(self, position):
        """
        If there is a stone at the given position tuple, highlights the group
        :param position: A position tuple or string indicating a
                         single stone in the group
        :return: Returns None
        """
        index = self.index_from_position_tuple(position)
        stone = self.get(index)
        group = stone.group
        if stone.color == StoneColor.black:
            highlight_color = StoneColor.highlight_black
        else:
            highlight_color = StoneColor.highlight_white
        for stone_index in group.members:
            self.get(stone_index).color = highlight_color

    def group_liberties(self, index):
        """
        Counts the liberties for a group
        :param index: The index of a single stone in the group
        :return: An integer representing the number of unique liberties
        """
        group = self.get(index).group
        liberties = set()
        for i in group.members:
            cardinal_indices = self.cardinal_indices(i)
            for ci in cardinal_indices:
                if self.get(ci) is None:
                    liberties.add(ci)
        return len(liberties)

    def group_captured(self, index):
        """
        Tests to see if a group is captured
        :param index: The index of a stone in the group
        :return: True if the group has been captured, False if it has not
        """
        return self.group_liberties(index) == 0

    def remove_group(self, index):
        """
        Removes a captured group from the board
        :param index: The index of a single stone from the group to be removed
        :return: Returns None
        """
        group = self.get(index).group
        for stone_index in group.members:
            self.board[stone_index] = None

    def board_string(self):
        """
        Creates a compact string of the current board positions, useful
        in recognizing Ko and for keeping game records
        :return: A string summarizing the current board positions
        """
        s = ""
        for i, v in enumerate(self.board):
            if i % 81 == 0:
                s += "\n"
            if v is None:
                s += "0"
            else:
                if v.color == StoneColor.black:
                    s += "1"
                else:
                    s += "2"
        return s