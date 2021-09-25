from .Map import Map_Obj
from .SearchNode import SearchNode
from .State import State

import time

class Search():
    """ Represents a search algorithm """

    def __init__(self, mp, filepath, max_iterations=1000, animate=False):
        self.mp = mp
        self.goal_pos = tuple(self.mp.get_goal_pos())
        self.open_nodes = []
        self.closed_nodes = []
        self.pos_to_obj = {}
        self.filepath = filepath
        self.max_iterations = max_iterations
        self.animate = animate

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
        iterations = 0
        while iterations < self.max_iterations:
            iterations += 1
            if self.animate:
                self.save_img(self.filepath, iterations)
            assert self.open_nodes  # Throws exception if array is empty
            x = self.pop_open()  # Pops open node with lowest cost
            self.push_to_closed(x)
            if x.get_pos() == self.goal_pos:
                return x
            succ = self.mp.get_adjacent_pos(x.get_pos())  # Same as generate_all_successors(X) in assignment
            for s_pos in succ:
                if s_pos in self.pos_to_obj:
                    # TODO: CHECK FOR DIFFERENCE IN STATE?
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
                elif x.g + self.get_arc_cost(x.pos, s.pos) < s.g:     # TODO: endre 1 til arc-cost
                    self.attach_and_eval(s, x)
                    if s in self.closed_nodes:
                        self.propagate_path_improvements(s)

    def find_best_path(self):
        start_time = time.time()
        best_path = []
        self.save_img(best_path, self.max_iterations*3)
        goal = self.best_first_search()
        best_path.append(goal.pos)
        parent = goal.parent
        iterations = self.max_iterations    # To distinguish between solution and search-frames
        while parent:
            iterations += 1
            if self.animate:
                self.save_img(best_path, iterations)
            best_path.append(parent.pos)
            parent = parent.parent
        best_path.reverse()
        self.save_img(best_path, iterations*2)
         # if self.animate:
        # self.mp.animate_search(self.filepath)
        print("--- %s seconds --- TOTAL ALGO TIME" % (time.time() - start_time))
        return best_path

    def attach_and_eval(self, c, p):
        c.parent = p
        c.g = p.g + self.get_arc_cost(p.pos, c.pos)   # TODO: Change 1 to arc-cost
        c.h = self.h(c.get_pos())
        c.f = c.g + c.h

    def propagate_path_improvements(self, p):
        for c in p.kids:
            arc_cost = self.get_arc_cost(p.pos, c.pos)
            if p.g + arc_cost < c.g:   # TODO: Change 1 to arc-cost
                c.p = p
                c.g = p.g + arc_cost   # TODO: Change 1 to arc-cost
                c.f = c.g + c.h
                self.propagate_path_improvements(c)

    def h(self, x):
        return self._manhattan_distance(x, self.mp.get_goal_pos())

    def _manhattan_distance(self, a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def get_arc_cost(self, a, b):
        return self.mp.int_map[b[0], b[1]]

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

    def save_img(self, path, nr):
        closed_nodes_pos = [node.pos for node in self.closed_nodes]
        str_map = self.mp.incorporate_search(self.mp.str_map, closed_nodes_pos, path)
        print(str_map)
        self.mp.save_map(str_map, nr, self.filepath)


