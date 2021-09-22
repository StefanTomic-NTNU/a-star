

class States():
    """ Represents the different states in searching the graph """

    def __init__(self, open, closed):
        self.open = open #list of searchnodes
        self.closed = closed #list of searchnodes