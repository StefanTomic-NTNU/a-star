from .Map import Map_Obj
from .SearchNode import SearchNode
from .State import State


class Search():
    """ Represents a search algorithm """

    def __init__(self, mp):
        self.mp = mp
        self.goal_pos = self.mp.get_goal_pos()
        self.open_nodes = []
        self.closed_nodes = []
        super(self)

    def best_first_search(self):
        """ Implementation of pseudocode in part 1 of assignment """

        # Creating start node
        state0 = State([])
        pos0 = self.mp.get_start_pos()
        children0 = self.mp.get_adjacent_pos(pos0)
        g = 0
        h = self.h(pos0)
        f = g + h
        n0 = SearchNode(state0, g, h, f, None, children0, pos0)
        self.push_to_open(n0)

        # Agenda loop:
        solution = False    # variable might be redundant
        while not solution:
            assert self.open_nodes      # Throws exception if array is empty
            x = self.pop_open()         # Pops open node with lowest cost
            self.push_to_closed(x)
            if x.get_pos() == self.goal_pos:
                return x    # TODO: Save solution path
            succ = self.mp.get_adjacent_nodes(x.get_pos())   # Same as generate_all_successors(X) in assignment
            # TODO: IMPLEMENT HASHMAP/DICT FROM POSITION TO NODE TO CHECK IF SEARCH_NODE OBJECT IS ALREADY CONSTRUCTED
            # TODO: IMPLEMENT REST OF FUNC

    def attach_and_eval(self, c, p):
        # TODO: IMPLEMENT METHOD
        pass

    def propagate_path_improvements(self, p):
        # TODO: IMPLEMENT METHOD
        pass

    def h(self, x):
        return self._manhattan_distance(x, self.mp.get_goal_pos())

    def _manhattan_distance(self, a, b):
        return sum(abs(b[0] - a[0]), abs(b[1] - a[1]))

    def __sort_open(self):
        """ Sorts open in ascending order """
        self.open_nodes.sort()

    def pop_open(self):
        """ Pops first (top) element in open"""
        return self.open_nodes.pop(0)

    def push_to_open(self, node):
        """ Adds SearchNode to open """
        self.open_nodes.append(node)
        self.__sort_open()

    def push_to_closed(self, node):
        """ Adds SearchNode to open """
        self.closed_nodes.append(node)
