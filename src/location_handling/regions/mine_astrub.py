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

    MINE_MAP_EXIT_POS = [
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
