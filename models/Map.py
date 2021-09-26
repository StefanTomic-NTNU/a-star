import numpy as np

np.set_printoptions(threshold=np.inf, linewidth=300)

import pandas as pd
from PIL import Image

# Imports for animation and file-handling:
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as an
import matplotlib.patches as patch

class Map_Obj():
    def __init__(self, task=1, resources_path=''):
        self.start_pos, self.goal_pos, self.end_goal_pos, self.path_to_map = self.fill_critical_positions(
            task)
        self.task = task    # Attribute added for ease of file-handling
        self.int_map, self.str_map = self.read_map(resources_path + self.path_to_map)
        self.tmp_cell_value = self.get_cell_value(self.goal_pos)
        self.set_cell_value(self.start_pos, ' S ')
        self.set_cell_value(self.goal_pos, ' G ')
        self.tick_counter = 0

    def read_map(self, path):
        """
        Reads maps specified in path from file, converts them to a numpy array and a string array. Then replaces
        specific values in the string array with predefined values more suitable for printing.
        :param path: Path to .csv maps
        :return: the integer map and string map
        """
        # Read map from provided csv file
        df = pd.read_csv(path, index_col=None,
                         header=None)  # ,error_bad_lines=False)
        # Convert pandas dataframe to numpy array
        data = df.values
        # Convert numpy array to string to make it more human readable
        data_str = data.astype(str)
        # Replace numeric values with more human readable symbols
        data_str[data_str == '-1'] = ' # '
        data_str[data_str == '1'] = ' . '
        data_str[data_str == '2'] = ' , '
        data_str[data_str == '3'] = ' : '
        data_str[data_str == '4'] = ' ; '
        return data, data_str

    def fill_critical_positions(self, task):
        """
        Fills the important positions for the current task. Given the task, the path to the correct map is set, and the
        start, goal and eventual end_goal positions are set.
        :param task: The task we are currently solving
        :return: Start position, Initial goal position, End goal position, path to map for current task.
        """
        if task == 1:
            start_pos = [27, 18]
            goal_pos = [40, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_1.csv'
        elif task == 2:
            start_pos = [40, 32]
            goal_pos = [8, 5]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_1.csv'
        elif task == 3:
            start_pos = [28, 32]
            goal_pos = [6, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_2.csv'
        elif task == 4:
            start_pos = [28, 32]
            goal_pos = [6, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_Edgar_full.csv'
        elif task == 5:
            start_pos = [14, 18]
            goal_pos = [6, 36]
            end_goal_pos = [6, 7]
            path_to_map = 'Samfundet_map_2.csv'

        return start_pos, goal_pos, end_goal_pos, path_to_map

    def get_cell_value(self, pos):
        return self.int_map[pos[0], pos[1]]

    def get_goal_pos(self):
        return self.goal_pos

    def get_start_pos(self):
        return self.start_pos

    def get_end_goal_pos(self):
        return self.end_goal_pos

    def get_maps(self):
        # Return the map in both int and string format
        return self.int_map, self.str_map

    def move_goal_pos(self, pos):
        """
        Moves the goal position towards end_goal position. Moves the current goal position and replaces its previous
        position with the previous values for correct printing.
        :param pos: position to move current_goal to
        :return: nothing.
        """
        tmp_val = self.tmp_cell_value
        tmp_pos = self.goal_pos
        self.tmp_cell_value = self.get_cell_value(pos)
        self.goal_pos = [pos[0], pos[1]]
        self.replace_map_values(tmp_pos, tmp_val, self.goal_pos)

    def set_cell_value(self, pos, value, str_map=True):
        if str_map:
            self.str_map[pos[0], pos[1]] = value
        else:
            self.int_map[pos[0], pos[1]] = value

    def print_map(self, map_to_print):
        # For every column in provided map, print it
        for column in map_to_print:
            print(column)

    def pick_move(self):
        """
        A function used for moving the goal position. It moves the current goal position towards the end_goal position.
        :return: Next coordinates for the goal position.
        """
        if self.goal_pos[0] < self.end_goal_pos[0]:
            return [self.goal_pos[0] + 1, self.goal_pos[1]]
        elif self.goal_pos[0] > self.end_goal_pos[0]:
            return [self.goal_pos[0] - 1, self.goal_pos[1]]
        elif self.goal_pos[1] < self.end_goal_pos[1]:
            return [self.goal_pos[0], self.goal_pos[1] + 1]
        else:
            return [self.goal_pos[0], self.goal_pos[1] - 1]

    def replace_map_values(self, pos, value, goal_pos):
        """
        Replaces the values in the two maps at the coordinates provided with the values provided.
        :param pos: coordinates for where we want to change the values
        :param value: the value we want to change to
        :param goal_pos: The coordinate of the current goal
        :return: nothing.
        """
        if value == 1:
            str_value = ' . '
        elif value == 2:
            str_value = ' , '
        elif value == 3:
            str_value = ' : '
        elif value == 4:
            str_value = ' ; '
        else:
            str_value = str(value)
        self.int_map[pos[0]][pos[1]] = value
        self.str_map[pos[0]][pos[1]] = str_value
        self.str_map[goal_pos[0], goal_pos[1]] = ' G '

    def tick(self):
        """
        Moves the current goal position every 4th call if current goal position is not already at the end_goal position.
        :return: current goal position
        """
        # For every 4th call, actually do something
        if self.tick_counter % 4 == 0:
            # The end_goal_pos is not set
            if self.end_goal_pos is None:
                return self.goal_pos
            # The current goal is at the end_goal
            elif self.end_goal_pos == self.goal_pos:
                return self.goal_pos
            else:
                # Move current goal position
                move = self.pick_move()
                self.move_goal_pos(move)
                # print(self.goal_pos)
        self.tick_counter += 1

        return self.goal_pos

    def set_start_pos_str_marker(self, start_pos, map):
        # Attempt to set the start position on the map
        if self.int_map[start_pos[0]][start_pos[1]] == -1:
            self.print_map(self.str_map)
            print('The selected start position, ' + str(start_pos) +
                  ' is not a valid position on the current map.')
            exit()
        else:
            map[start_pos[0]][start_pos[1]] = ' S '

    def set_goal_pos_str_marker(self, goal_pos, map):
        # Attempt to set the goal position on the map
        if self.int_map[goal_pos[0]][goal_pos[1]] == -1:
            self.print_map(self.str_map)
            print('The selected goal position, ' + str(goal_pos) +
                  ' is not a valid position on the current map.')
            exit()
        else:
            map[goal_pos[0]][goal_pos[1]] = ' G '

    def show_map(self, map=None):
        """
        A function used to draw the map as an image and show it.
        :param map: map to use
        :return: nothing.
        """
        # If a map is provided, set the goal and start positions
        if map is not None:
            self.set_start_pos_str_marker(self.start_pos, map)
            self.set_goal_pos_str_marker(self.goal_pos, map)
        # If no map is provided, use string_map
        else:
            map = self.str_map

        # Define width and height of image
        width = map.shape[1]
        height = map.shape[0]
        # Define scale of the image
        scale = 20
        # Create an all-yellow image
        image = Image.new('RGB', (width * scale, height * scale),
                          (255, 255, 0))
        # Load image
        pixels = image.load()

        # Define what colors to give to different values of the string map (undefined values will remain yellow, this is
        # how the yellow path is painted)
        colors = {
            ' # ': (211, 33, 45),
            ' . ': (215, 215, 215),
            ' , ': (166, 166, 166),
            ' : ': (96, 96, 96),
            ' ; ': (36, 36, 36),
            ' S ': (255, 0, 255),
            ' G ': (0, 128, 255)
        }
        # Go through image and set pixel color for every position
        for y in range(height):
            for x in range(width):
                if map[y][x] not in colors: continue
                for i in range(scale):
                    for j in range(scale):
                        pixels[x * scale + i,
                               y * scale + j] = colors[map[y][x]]
        # Show image
        image.show()

    def get_adjacent_pos(self, pos):
        """
        A function used to get positions adjacent to given position (kids)
        :param: pos: tuple representing x,y coordinates
        :return: position of adjacent (non-negative) nodes
        """
        assert self.int_map[pos[0], pos[1]] != -1
        result = []
        n = [0, 1, 0, -1, 0]
        for i in range(0, len(n) - 1):
            adj_pos = (pos[0] + n[i], pos[1] + n[i + 1])
            if self.int_map[adj_pos[0], adj_pos[1]] != -1:
                result.append(adj_pos)
        return result

    def save_map_chained(self, str_map, extra, nr, root_filepath, delta_closed, delta_path):
        """
        Generates images from str map, but saves time by only being concerned about
        what has changes since last iteration
        :param str_map: String of map
        :param extra: Extra character used in filenames to distinguish the different phases of the search
        :param nr: Frame nr
        :param root_filepath: Filepath to root of project
        :param delta_closed: Change in closed_nodes list since last frame
        :param delta_path: Change in best_path list since last frame
        :return: Nothing
        """
        width = str_map.shape[1]
        height = str_map.shape[0]

        start_tuple = tuple(self.start_pos)
        goal_tuple = tuple(self.goal_pos)

        # Define scale of the image
        scale = 20

        chained_img = True
        try:
            fp_old = root_filepath + r'\\resources\\image\\task' + str(self.task) + r'\\frame_' + extra + str(nr - 1).rjust(4, '0') + '.png'
            image = Image.open(fp_old)
        except FileNotFoundError:
            chained_img = False
            image = Image.new('RGB', (width * scale, height * scale),
                              (255, 255, 0))

        pixels = image.load()

        colors = {
            ' # ': (211, 33, 45),
            ' . ': (215, 215, 215),
            ' , ': (166, 166, 166),
            ' : ': (96, 96, 96),
            ' ; ': (36, 36, 36),
            ' S ': (255, 0, 255),
            ' G ': (0, 128, 255),
            ' E ': (255, 123, 27),
            ' P ': (3, 223, 159)
        }

        if not chained_img:
            for y in range(height):
                for x in range(width):
                    if str_map[y][x] not in colors: continue
                    for i in range(scale):
                        for j in range(scale):
                            pixels[x * scale + i,
                                   y * scale + j] = colors[str_map[y][x]]

        else:
            for (y, x) in delta_closed:
                if (y, x) == start_tuple or (y, x) == goal_tuple: continue
                for i in range(scale):
                    for j in range(scale):
                        pixels[x * scale + i,
                               y * scale + j] = (255, 123, 27)

            for (y, x) in delta_path:
                if (y, x) == start_tuple or (y, x) == goal_tuple: continue
                for i in range(scale):
                    for j in range(scale):
                        pixels[x * scale + i,
                               y * scale + j] = (3, 223, 159)

        fp = root_filepath + r'\\resources\\image\\task' + str(self.task) + r'\\frame_' + extra + str(nr).rjust(4, '0') + '.png'
        image.save(fp, 'png')

    def incorporate_search(self, str_map, searched_pos, path):
        """
        Incorporates the search-process into provided string map. Used for generating images/frames
        :param str_map: string map
        :param searched_pos: searched positions
        :param path: found path
        :return: Modified string map
        """
        start = tuple(self.start_pos)
        goal = tuple(self.goal_pos)
        for y, x_list in enumerate(str_map):
            for x, value in enumerate(x_list):
                if (y, x) in searched_pos and (y, x) != start and (y, x) != goal:
                    str_map[y][x] = ' E '
        if path:
            for y, x_list in enumerate(str_map):
                for x, value in enumerate(x_list):
                    if (y, x) in path and (y, x) != start and (y, x) != goal:
                        str_map[y][x] = ' P '
        return str_map

    def animate_search(self, root_filepath):
        """
        Animates images in resources into gif
        :param root_filepath: Filepath to root of project
        :return: Nothing
        """
        print('Animating')

        fp_out = root_filepath + r'\\resources\\gif\\task' + str(self.task) + r'\\animation.gif'

        figure = plt.figure(figsize=(8, 7))
        plt.xticks([]), plt.yticks([])

        start = patch.Patch(color='purple', label='Start')
        goal = patch.Patch(color='blue', label='Goal')
        wall = patch.Patch(color='red', label='Wall')
        arc_cost = patch.Patch(color='gray', label='Arch cost, \ndarker is higher')
        explored = patch.Patch(color='orange', label='Explored')
        best_path = patch.Patch(color='turquoise', label='Best path')

        plt.title(label='A* on task ' + str(self.task))
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), handles=[start, goal, wall, arc_cost, explored, best_path])
        plt.tight_layout()

        filepaths = sorted(glob.glob(root_filepath + r'\\resources\\image\\task' + str(self.task) + r'\\' + '*'))

        img = plt.imread(filepaths[0])
        imgplot = plt.imshow(img, interpolation='nearest')

        def load_imgplot(frame, *fargs):
            img = mpimg.imread(filepaths[frame])
            imgplot.set_data(img)
            return imgplot

        anim = an.FuncAnimation(figure, load_imgplot, frames=len(filepaths), interval=24, repeat=True)

        anim.save(fp_out)
