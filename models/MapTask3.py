from .Map import *

#task 3 change map
m = Map_Obj(task=3)

x = [16, 28]
m.replace_map_values(x, 3, m.goal_pos)

x[1] = 27
for i in range(0, 12):
    x[0] = 16 + i
    m.replace_map_values(x, 3, m.goal_pos)
for j in range(0, 5):
    x[1] = 27 - j
    m.replace_map_values(x, 3, m.goal_pos)

m.show_map()

