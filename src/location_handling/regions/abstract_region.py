import itertools
import math
from typing import List

from src.location_handling.city.abstract_city import AbstractCity
from src.utils.Displayer import Displayer
from src.utils.JsonHandler import JsonHandler
from src.utils.utils_fct import get_distance


class AbstractRegion:
    NAME: str
    CITY: str
    IS_REVERSE_PATH = False

    # LOCATIONS
    PHOENIX_STATUE_LOCATION: list
    CHECKPOINT: list
    RESSOURCES_LOCATIONS: dict

    # IMAGES
    PHOENIX_STATUE_IMAGE: str

    def __init__(self, ressources):
        self.path = []
        self.ressources = ressources

        self.set_path(ressources)

    def get_phoenix_path(self):
        """ get to phoenix statue from requested location """
        return [self.PHOENIX_STATUE_LOCATION]

    def get_path(self, from_location, to_location):
        return [to_location]

    def get_aiming_location(self, from_location, to_location):
        return to_location

    # ==================================================================================================================
    # INITIALIZATION
    def set_path(self, ressources: list):
        """ get unique position of each ressources """
        path = self.RESSOURCES_LOCATIONS[ressources[0]]
        if len(ressources) > 1:
            for ressource_name in ressources:
                path = self.get_best_path_2(path, self.RESSOURCES_LOCATIONS[ressource_name])

        self.path = path

        # path = JsonHandler.get_json_path(ressources, self.NAME)
        # if path is not None:
        #     self.path = path
        #     print(f'Loaded path : {self.path}')
        #     return
        #
        # # self.path = self.get_best_path(self.path, from_checkpoint=self.CHECKPOINT)
        # JsonHandler.save_json_path(ressources, self.NAME, self.path)
        # print(f'Path : {path}')

    @staticmethod
    def calculate_detour(loc1, loc2, mid_loc) -> int:
        """
        On a path from a location to another, calculate detour that passing threw a third location would take
        :param loc1:    start location
        :param loc2:    end location
        :param mid_loc: location to pass through

        :return:    minimum detour that it would take
        """
        x_min = min(loc1[0], loc2[0])
        x_max = max(loc1[0], loc2[0])
        y_min = min(loc1[1], loc2[1])
        y_max = max(loc1[1], loc2[1])

        # check if is in path (= no detour)
        if x_max >= mid_loc[0] >= x_min and y_max >= mid_loc[1] >= y_min:
            return 0

        min_distance = math.inf
        for x in range(abs(x_max - x_min) + 1):
            for y in range(abs(y_max - y_min) + 1):
                distance = get_distance([x + x_min, y + y_min], mid_loc) * 2
                if distance < min_distance:
                    min_distance = distance
        return min_distance

    def get_best_path_2(self, path1, path2) -> list:
        """ get the best common path between 2 paths """
        # remove common values
        path2 = [x for x in path2 if x not in path1]

        for val in path2:
            index = 0
            min_detour = math.inf
            for i in range(len(path1)):
                j = (i + 1) % len(path1)

                detour = self.calculate_detour(path1[i], path1[j], val)

                if detour == 0:
                    index = j
                    break

                elif detour < min_detour:
                    min_detour = detour
                    index = j

            if index == 0:
                path1.append(val)
            else:
                path1.insert(index, val)

        return path1

    @staticmethod
    def get_best_path(all_pos: List[List[int]], from_checkpoint: List[int]) -> List[List[int]]:
        """
        calculate most optimized path for all given positions
        :param all_pos:         list of all positions that the bot is supposed to go to
        :param from_checkpoint: checkpoint from where the char arrives
        :return:
        """

        Displayer.print('calculating best path... ', end='')
        n_factorial = 1
        for i in range(1, len(all_pos)):
            n_factorial = n_factorial * i

        # get index of the position closest to the checkpoint
        start_pos_index = None
        for i in range(len(all_pos)):
            if start_pos_index is None or get_distance(all_pos[start_pos_index], from_checkpoint) > get_distance(all_pos[i], from_checkpoint):
                start_pos_index = i

        # pop closest position from all positions as start position
        start_pos = all_pos.pop(0)

        # from remaining positions, calculate the shortest path
        best_distance = math.inf
        best_path = []
        i = 0
        for path in itertools.permutations(all_pos, len(all_pos)):
            print(f"{i} / {n_factorial}", end='\r')
            i += 1
            distance = 0
            last_pos = start_pos
            for pos in path:
                relative_distance = get_distance(pos, last_pos)
                if relative_distance > 6:
                    distance = math.inf
                    break

                distance += relative_distance

                if distance >= best_distance:
                    distance = math.inf
                    break

                last_pos = pos

            # -- get back to start position
            distance += get_distance(start_pos, last_pos)

            # -- check if distance is shorter
            if distance < best_distance:
                best_path = list(path)
                best_distance = distance

        print("done !")
        return [start_pos] + best_path


    @staticmethod
    def in_between(location, top_corner, bottom_corner):
        return bottom_corner[0] >= location[0] >= top_corner[0] \
            and bottom_corner[1] >= location[1] >= top_corner[1]
