import os

from models.Map import Map_Obj
from models.Search import Search

if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__))
    mp = Map_Obj(1, resources_path='./resources/')
    # mp.print_map(mp.str_map)
    # mp.show_map()
    search = Search(mp, filepath)
    best_path = search.find_best_path()
    print(best_path)
    # mp.show_map()
    # search = Search(mp)
