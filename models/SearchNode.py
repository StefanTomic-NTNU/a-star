

class SearchNode():
    """ Represents the searchable nodes in a graph """

    def __init__(self, state, g, h, status, parent, kids, pos):
        self.state = state      # object state check State.py
        self.h = h
        self.g = g
        self.f = g + h          # estimated total cost of a solution path
        self.status = status    # string "OPEN" or "CLOSE"
        self.parent = parent    # pointer to best parent node
        self.kids = kids        # a list maybe
        self.pos = pos          # position in 2D array

    def get_pos(self):
        return self.pos
