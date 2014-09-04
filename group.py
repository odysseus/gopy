class Group(object):
    """
    The group class represents one or more contiguous stones
    """
    def __init__(self, board):
        """
        A group of contiguous stones
        :param board: The board on which the group is contained
        :ivar members: A set of indices for the stones in the group
        :return: An initialized group
        """
        self.board = board
        self.members = set()
        self.size = len(self.members)

    def add_member(self, stone):
        """
        Adds a stone to the set of member stones
        :param stone: A single stone object
        :return: Returns None
        """
        self.members.add(stone)

    def add_members(self, stones):
        """
        Adds multiple stones to the set of members
        :param stones: A set of stones to be added
        :return: Returns None
        """
        self.members.update(stones)