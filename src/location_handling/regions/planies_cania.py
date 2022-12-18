from src.enum.actions import Actions
from src.enum.images import Images
from src.location_handling.city.bonta import Bonta
from src.location_handling.regions.abstract_region import AbstractRegion
from src.enum.locations import Locations
from src.enum.regions import Regions
from src.enum.ressources import Ressources
from src.utils.ErrorHandler import ErrorHandler


class PlainesCania(AbstractRegion):
    NAME = Regions.PLAINES_CANIA
    CITY = Bonta.NAME
    PHOENIX_STATUE_LOCATION: list = [-10, -54]
    CHECKPOINT: list = Locations.ZAAPS[Regions.PLAINES_CANIA]

    PHOENIX_STATUE_IMAGE = Images.get_screenshot(Images.PHOENIX_STATUE_2)

    RESSOURCES_LOCATIONS: dict = {
            Ressources.MALT: [
                [-27, -43],
                [-27, -42],
                [-25, -42],
                [-26, -40],
                [-25, -39],
                [-22, -39],
            ],

            Ressources.SEIGLE: [
                [-30, -41],
                [-30, -39],
                [-28, -39],
                [-28, -40],
                [-26, -38],
                [-25, -40],
                [-28, -44],
                [-27, -42],
                [-26, -42],
                [-24, -42],
                [-25, -43],
                [-25, -44],
                [-23, -40],
                [-23, -39],
            ],

            Ressources.CHANVRE: [
                [-28, -42],
                [-26, -43],
                [-23, -42],
                [-22, -39],
            ],
        }

    def get_path(self, from_location, to_location):
        path = []
        if Bonta.is_in_city(from_location):
            if Bonta.is_in_city(to_location):
                ErrorHandler.warning("asking for a city movement in the region")
                return Bonta.get_path(from_location, to_location)

            path.append(Actions.TAKE_RECALL_POTION)

        path.append(to_location)