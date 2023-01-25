from src.enum.actions import Actions
from src.enum.images import Images
from src.location_handling.city.bonta import Bonta
from src.location_handling.regions.abstract_region import AbstractRegion
from src.enum.locations import Locations
from src.enum.regions import Regions
from src.enum.ressources import Ressources


class PlainesCania(AbstractRegion):
    NAME = Regions.PLAINES_CANIA
    CITY = Bonta.NAME

    PHOENIX_STATUE_LOCATION: list = [-10, -54]
    CHECKPOINT: list = Locations.ZAAPS[Regions.PLAINES_CANIA]

    PHOENIX_STATUE_IMAGE = Images.PHOENIX_STATUE_2

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

        Ressources.EAU_POTABLE: [
            [-26, -38],
            [-28, -38],
            [-29, -40],
            [-30, -43],
            [-26, -41],
            [-27, -46],
        ]
    }

    def get_aiming_location(self, from_location, to_location):
        if Bonta.is_in_city(from_location) or Bonta.is_in_city(to_location):
            return Bonta.get_aiming_location(from_location, to_location)

        if from_location == self.PHOENIX_STATUE_LOCATION:
            return Actions.TAKE_RECALL_POTION

        return to_location