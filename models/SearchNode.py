

class SearchNode():
    """ Represents the searchable nodes in a graph """

    def __init__(self, g, h, parent, kids, pos):
        self.h = h
        self.g = g
        self.f = g + h          # estimated total cost of a solution path
        self.parent = parent    # pointer to best parent node
        self.kids = kids        # a list maybe
        self.pos = pos          # position in 2D array

    def get_pos(self):
        return self.pos
