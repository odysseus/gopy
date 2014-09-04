"""
The group object represents one or more contiguous stones
"""

class Group(object):
    def __init__(self, board):
        self.board = board
        self.members = []
        self.size = len(self.members)