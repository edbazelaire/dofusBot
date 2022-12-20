from src.enum.actions import Actions
from src.enum.regions import Regions
from src.enum.ressources import Ressources
from src.location_handling.regions.abstract_region import AbstractRegion


class MineAstrub(AbstractRegion):
    NAME: str = Regions.MINE_ASTRUB
    CITY: str = 'Astrub'

    # LOCATIONS
    PHOENIX_STATUE_LOCATION: list = [2, -14]
    CHECKPOINT: list

    # MINE SPECIFICS
    MINE_LOCATION = [1, -17]
    MINE_ENTER_CLICK_POS = (1122, 625)
    MINE_EXIT_CLICK_POS = (459, 797)

    MINE_MAP_ENTER_POS = [
        (1472, 250),
        (1508, 580)
    ]

    MINE_EXIT_POS = [
        (363, 570),
        (531, 255)
    ]

    MINE_PATH = [
        [1, -17],
        [2, -18],
        [3, -18]
    ]

    RESSOURCES_LOCATIONS: dict = {
        Ressources.FER: MINE_PATH
    }

    # IMAGES
    PHOENIX_STATUE_IMAGE: str

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
            path.append((Actions.CLICK_ON, self.MINE_EXIT_POS))
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
                path.append(self.MINE_EXIT_POS[i])
