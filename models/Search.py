from .Map import Map_Obj
from .SearchNode import SearchNode
from .State import State


class Search():
    """ Represents a search algorithm """

    def __init__(self, mp):
        self.mp = mp
        self.goal_pos = tuple(self.mp.get_goal_pos())
        self.open_nodes = []
        self.closed_nodes = []
        self.pos_to_obj = {}

    def best_first_search(self):
        """ Implementation of pseudocode in part 1 of assignment """

        # Creating start node
        state0 = State([])
        pos0 = tuple(self.mp.get_start_pos())
        children0 = self.mp.get_adjacent_pos(pos0)
        g = 0
        h = self.h(pos0)
        f = g + h
        n0 = SearchNode(state0, g, h, f, None, children0, pos0)
        self.pos_to_obj[tuple(pos0)] = n0
        self.push_to_open(n0)

        # Agenda loop:
        solution = False  # variable might be redundant
        while not solution:
            assert self.open_nodes  # Throws exception if array is empty
            x = self.pop_open()  # Pops open node with lowest cost
            self.push_to_closed(x)
            if x.get_pos() == self.goal_pos:
                return x  # TODO: Save solution path. Maybe not, just store as parent
            succ = self.mp.get_adjacent_pos(x.get_pos())  # Same as generate_all_successors(X) in assignment
            for s_pos in succ:
                if s_pos in self.pos_to_obj:
                    # TODO: CHECK FOR DIFFERENCE IN STATE
                    s = self.pos_to_obj[s_pos]  # Might have to create other variable instead
                    x.kids.append(s)
                else:   # Construct new node
                    g = x.g + 1  # TODO: change 1 to arc-cost
                    h = self.h(s_pos)
                    f = g + h
                    kids = self.mp.get_adjacent_pos(s_pos)
                    s = SearchNode(self.closed_nodes, g, h, f, x, kids, s_pos)
                    self.pos_to_obj[s_pos] = s
                if (s not in self.open_nodes) and (s not in self.closed_nodes):
                    self.attach_and_eval(s, x)
                    self.push_to_open(s)
                elif x.g + 1 < s.g:     # TODO: endre 1 til arc-cost
                    self.attach_and_eval(s, x)
                    if s in self.closed_nodes:
                        self.propagate_path_improvements(s)

    def find_best_path(self):
        best_path = []
        goal = self.best_first_search()
        best_path.append(goal.pos)
        parent = goal.parent
        while parent:
            print(parent.pos)
            best_path.append(parent.pos)
            parent = parent.parent
        return best_path

    def attach_and_eval(self, c, p):
        c.parent = p
        c.g = p.g + 1   # TODO: Change 1 to arc-cost
        c.h = self.h(c.get_pos())
        c.f = c.g + c.h

    def propagate_path_improvements(self, p):
        for c in p.kids:
            if p.g + 1 < c.g:   # TODO: Change 1 to arc-cost
                c.p = p
                c.g = p.g + 1   # TODO: Change 1 to arc-cost
                c.f = c.g + c.h
                self.propagate_path_improvements(c)

    def h(self, x):
        return self._manhattan_distance(x, self.mp.get_goal_pos())

    def _manhattan_distance(self, a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def __sort_open(self):
        """ Sorts open in ascending order """
        self.open_nodes.sort(key=lambda node: node.f)

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
