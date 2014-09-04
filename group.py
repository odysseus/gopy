class Group(object):
    """
    The group class represents one or more contiguous stones
    """
    def __init__(self, board):
        """
        A group of contiguous stones
        :param board: The board on which the group is contained
        :ivar members: A set of the stones contained in the group
        :return: An initialized group
        """
        self.board = board
        self.members = {}
        self.size = len(self.members)