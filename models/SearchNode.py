

class SearchNode():
    """ Represents the searchable nodes in a graph """

    def __init__(self, state, g, h, status, parent, kids):
        self.state = state #object state check States.py
        self.h = h
        self.g = g
        self.f = g + h # estimated total cost of a solution path
        self.parent = parent #pointer to best parent node
        self.status = status #string "OPEN" or "CLOSE"
        self.kids = kids #a list maybe
