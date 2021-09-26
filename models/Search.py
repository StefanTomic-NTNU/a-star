from .Map import Map_Obj
from .SearchNode import SearchNode

import time

class Search():
    """ Represents a search algorithm """

    def __init__(self, mp, root_filepath, max_iterations=1000, animate=False):
        self.mp = mp
        self.goal_pos = tuple(self.mp.get_goal_pos())
        self.open_nodes = []
        self.closed_nodes = []
        self.old_closed_nodes = []  # Used to get delta_closed for faster image gen
        self.pos_to_obj = {}
        self.root_filepath = root_filepath
        self.max_iterations = max_iterations
        self.animate = animate

    def best_first_search(self):
        """ Implementation of pseudocode in part 1 of assignment """

        print('Performing Best First Search on Task ' + str(self.mp.task) + '...')

        # Creating start node
        pos0 = tuple(self.mp.get_start_pos())
        children0 = self.mp.get_adjacent_pos(pos0)
        g = 0
        h = self.h(pos0)
        n0 = SearchNode(g, h, None, children0, pos0)
        self.pos_to_obj[tuple(pos0)] = n0
        self.push_to_open(n0)

        # Agenda loop:
        iterations = 0
        while iterations < self.max_iterations:
            self.mp.tick()
            self.goal_pos = tuple(self.mp.get_goal_pos())
            if self.animate:
                self.old_closed_nodes = self.closed_nodes.copy()
            iterations += 1
            assert self.open_nodes  # Throws exception if array is empty
            x = self.pop_open()  # Pops open node with lowest cost
            self.push_to_closed(x)
            if x.get_pos() == self.goal_pos:
                return x
            succ = self.mp.get_adjacent_pos(x.get_pos())  # Same as generate_all_successors(X) in assignment
            for s_pos in succ:
                if s_pos in self.pos_to_obj:
                    s = self.pos_to_obj[s_pos]  # Might have to create other variable instead
                    x.kids.append(s)
                else:   # Construct new node
                    g = x.g + 1
                    h = self.h(s_pos)
                    f = g + h
                    kids = self.mp.get_adjacent_pos(s_pos)
                    s = SearchNode(g, h, x, kids, s_pos)
                    self.pos_to_obj[s_pos] = s
                if (s not in self.open_nodes) and (s not in self.closed_nodes):
                    self.attach_and_eval(s, x)
                    self.push_to_open(s)
                elif x.g + self.get_arc_cost(x.pos, s.pos) < s.g:
                    self.attach_and_eval(s, x)
                    if s in self.closed_nodes:
                        self.propagate_path_improvements(s)
            if self.animate:
                self.save_img([], [], 'c', iterations)  # c for before path is found

    def find_best_path(self):
        """
        Parses the graph to find best path after running best_first_search to generate all the SearchNodes.
        :return: Shortest/best path
        """
        start_time = time.time()
        best_path = []
        old_best_path = []
        self.save_img(best_path, old_best_path, 'a', 0)     # a for initial
        goal = self.best_first_search()
        print('Goal reached!')
        best_path.append(goal.pos)
        parent = goal.parent
        iterations = self.max_iterations
        while parent:
            if self.animate:
                old_best_path = best_path.copy()
            iterations += 1
            best_path.append(parent.pos)
            if self.animate:
                self.save_img(best_path, old_best_path, 'e', iterations)    # e for path
            parent = parent.parent
        best_path.reverse()
        print('Best path found!')
        for i in range(0, 40):
            self.save_img(best_path, old_best_path, 'f', i)     # f for finish, some extra frames to pause at finish
        if self.animate:
            self.mp.animate_search(self.root_filepath)
        print("--- %s seconds --- TOTAL PROGRAM TIME FOR TASK" % (time.time() - start_time) + str(self.mp.task) + '\n')
        return best_path

    def attach_and_eval(self, c, p):
        c.parent = p
        c.g = p.g + self.get_arc_cost(p.pos, c.pos)
        c.h = self.h(c.get_pos())
        c.f = c.g + c.h

    def propagate_path_improvements(self, p):
        for c in p.kids:
            arc_cost = self.get_arc_cost(p.pos, c.pos)
            if p.g + arc_cost < c.g:
                c.p = p
                c.g = p.g + arc_cost
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

    def save_img(self, best_path, old_best_path, extra, nr):
        """
        Saves image of search-process by calling function in Map.py. This is used as frames in the animation
        :param best_path: Best path
        :param old_best_path: Previous best path. Necessary to get delta_path
        :param extra: Extra character used in filenames to distinguish the different phases of the search
        :param nr: Frame nr
        :return: Nothing
        """
        closed_nodes_pos = [node.pos for node in self.closed_nodes]
        str_map = self.mp.incorporate_search(self.mp.str_map, closed_nodes_pos, best_path)

        # Get delta_closed
        closed_nodes_set = set(self.closed_nodes)
        old_closed_nodes_set = set(self.old_closed_nodes)
        delta_closed = closed_nodes_set.difference(old_closed_nodes_set)
        delta_closed = [node.pos for node in delta_closed]

        # Get delta_path
        best_path_set = set(best_path)
        old_best_path_set = set(old_best_path)
        delta_path = best_path_set.difference(old_best_path_set)

        self.mp.save_map_chained(str_map, extra, nr, self.root_filepath, delta_closed, delta_path)
