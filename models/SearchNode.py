class SearchNode:
    """ Represents the searchable nodes in a graph """

    def __init__(self, g, h, parent, kids, pos):
        """
        :param g: float, Heuristic (estimate of distance to goal)
        :param h: float, Estimate of distance from start to node
        :param parent: SearchNode, pointer to best parent node
        :param kids: List of SearchNodes, List of children of this SearchNode
        :param pos: tuple of (y, x) coordinates. SearchNode's position in 2D array
        """
        self.h = h
        self.g = g
        self.f = g + h          # estimated total cost of a solution path
        self.parent = parent
        self.kids = kids
        self.pos = pos

    def get_pos(self):
        return self.pos
