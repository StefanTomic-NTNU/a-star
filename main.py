import os

from models.Map import Map_Obj
from models.Search import Search

if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__))

    # Task 1
    # mp1 = Map_Obj(1, resources_path='./resources/')
    # search1 = Search(mp1, filepath, animate=False)
    # best_path = search1.find_best_path()
    # print(best_path)

    # Task 2
    # mp2 = Map_Obj(2, resources_path='./resources/')
    # mp2.show_map()
    # search2 = Search(mp2, filepath)
    # best_path2 = search2.find_best_path()

    # Task 3
    mp3 = Map_Obj(3, resources_path='./resources/')
    mp3.show_map()
    search3 = Search(mp3, filepath)
    best_path3 = search3.find_best_path()
