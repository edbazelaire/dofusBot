from typing import List

from src.enum.actions import Actions
from src.location_handling.regions.abstract_region import AbstractRegion
from src.utils.ErrorHandler import ErrorHandler


class AbstractMine(AbstractRegion):
    # ENTER THE MINE
    MINE_LOCATION: list                 # word map location of the mine
    MINE_ENTER_CLICK_POS: tuple         # pos to click to enter the mine
    MINE_EXIT_CLICK_POS: tuple          # pos to click to exit the mine

    # PATH INSIDE THE MINE
    MINE_PATH = List[List[int]]         # location path inside the mine
    MINE_MAP_ENTER_POS: List[tuple]     # JUNCTION : screen position to click to get from map (n) to map (n+1)
    MINE_MAP_EXIT_POS: List[tuple]      # JUNCTION : screen position to click to get from map (n) to map (n-1)

    RESSOURCES_LOCATIONS: dict = {}

    def __init__(self, ressources):
        super().__init__(ressources)

        if len(self.MINE_MAP_ENTER_POS) != len(self.MINE_MAP_EXIT_POS):
            ErrorHandler.fatal_error(f'length of mine enter positions ({len(self.MINE_MAP_ENTER_POS)}) is not equal to '
                                     f'length of map exit positions ({self.MINE_MAP_EXIT_POS})')

        if len(self.MINE_PATH) - 1 != len(self.MINE_MAP_ENTER_POS):
            ErrorHandler.fatal_error(f'length of mine enter positions ({len(self.MINE_MAP_ENTER_POS)}) is not equal to '
                                     f'number of maps inside the mine - 1 ({self.MINE_PATH})')

    def get_path(self, from_location, to_location):
        """ get path from a position to another (add special locations to go to if there is obstacle in between) """
        path = []
        # get from OUTSIDE -> mine
        if to_location in self.MINE_PATH and from_location not in self.MINE_PATH:
            path.append(self.MINE_LOCATION)
            path.append((Actions.CLICK_ON, self.MINE_ENTER_CLICK_POS))
            path += self.get_path_in_mine(self.MINE_PATH[0], to_location)

        # from mine -> mine
        elif to_location in self.MINE_PATH and from_location in self.MINE_PATH:
            path += self.get_path_in_mine(self.MINE_PATH[0], to_location)

        # get from mine -> OUTSIDE
        elif from_location in self.MINE_PATH and to_location not in self.MINE_PATH:
            path += self.get_path_in_mine(from_location, self.MINE_PATH[0])
            path.append((Actions.CLICK_ON, self.MINE_MAP_EXIT_POS))
            path.append(to_location)

        return path

    def get_path_in_mine(self, from_location, to_location):
        index_start = self.MINE_PATH.index(from_location)
        index_end = self.MINE_PATH.index(to_location)

        path = []
        if index_start < index_end:
            for i in range(index_start, index_end):
                path.append(self.MINE_MAP_ENTER_POS[i])

        elif index_start > index_end:
            for i in range(index_start, index_end, -1):
                path.append(self.MINE_MAP_EXIT_POS[i])
