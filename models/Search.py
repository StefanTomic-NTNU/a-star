from .Map import Map_Obj
from .SearchNode import SearchNode
from .State import State


class Search():
    """ Represents a search algorithm """

    def __init__(self, mp):
        self.mp = mp
        self.closed = []
        self.open = []
        self.g = None
        self.h = self._manhattan_distance
        self.f = None
        state0 = State([], [])
        # children0 = self._get_adjacent_pos(mp.get_start_pos())
        n0 = SearchNode(state0, self.g, self.h, self.f, None, )
        self.open.append(n0)
        super(self)

    def best_first_search(self):
        """ Implementation of pseudocode in part 1 of assignment """
        pass

    def attach_and_eval(self, c, p):
        pass

    def propagate_path_improvements(self, p):
        pass

    def _manhattan_distance(self, a, b):
        pass

    def _get_adjacent_nodes(self, node):
        pass

    def __sort_open(self):
        """ Sorts open in ascending order """
        self.open.sort()

    def pop_open(self):
        """ Pops first (top) element in open"""
        self.open.pop(0)

    def add_to_open(self, seach_node):
        """ Adds SearchNode to open """
        self.open.append(seach_node)
        self.__sort_open()