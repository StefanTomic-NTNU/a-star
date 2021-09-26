import os

from models.Map import Map_Obj
from models.Search import Search

if __name__ == '__main__':
    root_filepath = os.path.dirname(os.path.abspath(__file__))
    csv_dir = './resources/csv/'

    # Task 1
    mp1 = Map_Obj(1, resources_path=csv_dir)
    search1 = Search(mp1, root_filepath, animate=True)
    best_path = search1.find_best_path()

    # Task 2
    mp2 = Map_Obj(2, resources_path=csv_dir)
    search2 = Search(mp2, root_filepath, animate=True)
    best_path2 = search2.find_best_path()

    # Task 3
    mp3 = Map_Obj(3, resources_path=csv_dir)
    search3 = Search(mp3, root_filepath, animate=True)
    best_path3 = search3.find_best_path()

    # Task 4
    mp4 = Map_Obj(4, resources_path=csv_dir)
    search4 = Search(mp4, root_filepath, animate=True)
    best_path4 = search4.find_best_path()
