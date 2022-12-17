from src.enum.images import Images
from src.enum.regions import Regions
from src.enum.ressources import Ressources
from src.location_handling.city.astrub import Astrub
from src.location_handling.regions.abstract_region import AbstractRegion


class ChampAstrub(AbstractRegion):
    NAME: str = Regions.CHAMP_ASTRUB
    CITY = Astrub.NAME

    # LOCATIONS
    PHOENIX_STATUE_LOCATION: list = [2, -14]
    CHECKPOINT: list = None         # TODO
    RESSOURCES_LOCATIONS = {
            Ressources.HOUBLON: [
                [6, -22],
                [5, -24],
                [5, -26],
                [4, -26],
                [4, -28],
                [3, -30],
                [5, -28],
                [8, -23],
            ],

            Ressources.SEIGLE: [
                [5, -25],
                [3, -27],
                [9, -22]
            ],

            Ressources.CHANVRE: [
                [7, -24],
            ],

            Ressources.BLE: [
                [5, -22],
                [3, -22],
                [3, -23],
                [4, -23],
                [5, -25],
                [3, -26],
                [4, -27],
                [4, -29],
                [4, -30],
                [5, -30],
                [6, -30],
                [6, -29],
                [6, -28],
                [5, -28],
                [7, -25],
                [7, -23],
            ],

            "fake": [
                [7, -23]
            ]
        }

    # IMAGES
    PHOENIX_STATUE_IMAGE: str = Images.get_screenshot(Images.PHOENIX_STATUE)

