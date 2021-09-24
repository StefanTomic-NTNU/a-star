from models.SearchNode import *
from models.States import *
from models.Node import *
from models.Map import *

class Search():
    """ Represents a search algorithm """

    def __init__(self):
        super(self)

    def setup_n0(self):
        open = []
        closed = []
        kids = []
        s = States(open, closed)
        sn = SearchNode(s, 0, 0, "CLOSED", "NONE", kids)
        return sn
    
    def gen_succ(self, x):
        #think it is x y coords
        cords = x.get_cords()
        cords_node = []
        temp_cord = []
        x1 = cords[0] + 1
        x2 = cords[0] - 1
        y1 = cords[1] + 1
        y2 = cords[1] - 1

        temp_cord.append(x1, cords[1])
        cords_node.append(temp_cord)
        temp_cord = []

        temp_cord.append(x2, cords[1])
        cords_node.append(temp_cord)
        temp_cord = []

        temp_cord.append(cords[0], y1)
        cords_node.append(temp_cord)
        temp_cord = []

        temp_cord.append(cords[0], y2)
        cords_node.append(temp_cord)
        temp_cord = []

        return cords_node

    def arc_cost(self, x, s):
        pass
    #define arc cost

    def attach_and_eval(self, C, P):
        #fix method
        C.addparent(P)
        C.g = P.g + self.arc_cost(P,C)
        C.calculate_h(1)
        C.calculate_f()
        pass

    def propagate_path_improvements(self, s):
        #def from text
        pass

    def best_first_search(self):
        m = Map_Obj()
        closed = []
        open = []
        SUCC = []
        node = Node(0, 0, 0, m.get_start_pos())
        node.calculate_h(1)
        node.calculate_f()
        open.append(node)
        
        #loop
        if(len(open) == 0):
            print("failed")
            return 0
        
        x = open.pop()
        closed.append(x)
        
        if x.get_cord() == m.get_end_goal_pos():
            print("finished")
            return 1
        SUCC = self.gen_succ(x)
        for i in SUCC:
            #if node created before
            x.kids().append(i)
            if not i in open and not i in closed:
                self.attach_and_eval(i, x)
                pass
            #else if x.g + self.arc_cost(x, i) < : find a way to generate g in S
                #self.attach_and_eval(i, x)
            if i in closed:
                self.propagate_path_improvements(i)






