from src.enum.actions import Actions
from src.enum.images import Images
from src.enum.locations import Locations
from src.enum.regions import Regions
from src.enum.ressources import Ressources
from src.location_handling.city.bonta import Bonta
from src.location_handling.city.village_des_eleveurs import VillageDesEleveurs
from src.location_handling.regions.abstract_region import AbstractRegion
from src.utils.utils_fct import in_between_loc


class MontagneKoalak(AbstractRegion):
    NAME = Regions.MONTAGNE_KOALAK
    CITY = VillageDesEleveurs.NAME

    PHOENIX_STATUE_LOCATION: list = [-10, 13]
    CHECKPOINT: list = Locations.ZAAPS[Regions.MONTAGNE_KOALAK]
    PHOENIX_STATUE_IMAGE = Images.PHOENIX_STATUE_1      # TODO

    RESSOURCES_LOCATIONS: dict = {
        Ressources.ORCHIDEE_FREYESQUE: [
            [-19, 0],
            [-20, 0],
            [-21, 0],
            [-22, 0],
            [-22, 1],
            [-23, 1],
            [-21, 1],
            [-20, 1],
            [-19, 1],
            [-19, 2],
            [-20, 2],
            [-21, 2],
            [-22, 2],
            [-23, 2],
            [-23, 3],
            [-22, 3],
            [-22, 4],
            [-21, 4],
            [-21, 3],
            [-20, 3],
            [-20, 4],
            [-19, 4],
            [-19, 3],
            [-18, 4],
            [-18, 6],
            [-17, 6],

        ]
    }

    def get_aiming_location(self, from_location, to_location):
        if Bonta.is_in_city(from_location) or Bonta.is_in_city(to_location):
            return Bonta.get_aiming_location(from_location, to_location)

        if in_between_loc(from_location, [-13, 13], [-10, 21]) and in_between_loc(to_location, [-23, -2], [-12, 12]):
            return Actions.TAKE_RECALL_POTION

        return to_location