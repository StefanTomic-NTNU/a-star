

class State():
    """ Represents the different states in searching the graph """

    def __init__(self, closed):
        # self.open = open        # list of searchnodes
        self.closed = closed    # list of searchnodes

    # def __sort_open(self):
    #     """ Sorts open in ascending order """
    #     self.open.sort()
    #
    # def pop_open(self):
    #     """ Pops first (top) element in open"""
    #     self.open.pop(0)
    #
    # def add_to_open(self, seach_node):
    #     """ Adds SearchNode to open """
    #     self.open.append(seach_node)
    #     self.__sort_open()
