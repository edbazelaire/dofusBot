import itertools
import math
from typing import List

from src.location_handling.city.abstract_city import AbstractCity
from src.utils.JsonHandler import JsonHandler
from src.utils.utils_fct import get_distance


class AbstractRegion:
    NAME: str
    CITY: AbstractCity

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

    # ==================================================================================================================
    # INITIALIZATION
    def set_path(self, ressources: list):
        """ get unique position of each ressources """
        for ressource_name in ressources:
            pos = self.RESSOURCES_LOCATIONS[ressource_name]
            [self.path.append(pos[i]) for i in range(len(pos)) if pos[i] not in self.path]

        path = JsonHandler.get_json_path(ressources, self.NAME)
        if path is not None:
            self.path = path
            print(f'Loaded path : {self.path}')
            return

        # self.path = self.get_best_path(self.path, from_checkpoint=self.CHECKPOINT)
        JsonHandler.save_json_path(ressources, self.NAME, self.path)
        print(f'Path : {path}')

    @staticmethod
    def get_best_path(all_pos: List[List[int]], from_checkpoint: List[int]) -> List[List[int]]:
        """
        calculate most optimized path for all given positions
        :param all_pos:         list of all positions that the bot is supposed to go to
        :param from_checkpoint: checkpoint from where the char arrives
        :return:
        """

        print('calculation best path...')

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
        for path in itertools.permutations(all_pos, len(all_pos)):
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

        return [start_pos] + best_path
