


class Node():

    def __init__(self, g, h, f, cord):
        self.g = g
        self.h = h
        self.f = f
        self.cord = cord
        self.kids = []


    def calculate_h(self, tilevalue):
        self.h = tilevalue

    def calculate_f(self):
        self.f = self.h + self.g

    def get_cord(self):
        return self.cord

    def get_kids(self):
        return self.kids
    