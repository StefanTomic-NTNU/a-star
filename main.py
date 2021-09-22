from models.Map import Map_Obj
from models.Search import Search

if __name__ == '__main__':
    mp = Map_Obj(1, resources_path='./resources/')
    mp.print_map(mp.str_map)
    print(mp.start_pos)
    print(mp.get_adjacent_pos([mp.start_pos[0], mp.start_pos[1]]))
    # search = Search(mp)
