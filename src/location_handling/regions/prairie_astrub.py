from src.enum.images import Images
from src.enum.regions import Regions
from src.enum.ressources import Ressources
from src.location_handling.city.astrub import Astrub
from src.location_handling.regions.abstract_region import AbstractRegion


class PrairieAstrub(AbstractRegion):
    NAME: str = Regions.PRAIRIE_ASTRUB
    CITY = Astrub.NAME

    # LOCATIONS
    PHOENIX_STATUE_LOCATION: list = [2, -14]
    RESSOURCES_LOCATIONS = {
        # PLANTS
        Ressources.ORTIE: [
            [5, -17],
            [6, -17],
            [3, -16],
            [2, -16],
            [2, -17],
            [1, -16],
            [1, -15],
            [2, -15],
            [3, -14],
            [4, -14],
            [4, -15],
            [5, -14],
            [6, -14],
            [6, -13],
            [5, -13],
            [4, -13],
            [3, -13],
            [3, -12],
            [4, -12],
            [5, -12],
            [5, -11],
            [3, -11],
            [3, -9],
            [3, -8],
            [3, -10],
            [4, -10],
            [5, -10],
            [5, -9],
            [5, -11],
            [6, -11],
            [6, -10],
            [6, -9],
            [7, -10],
            [7, -11],
            [8, -11],
            [8, -9],
            [8, -10],
            [9, -10],
            [9, -11],
            [9, -12],
            [8, -12],
            [8, -13],
            [9, -13],
            [10, -13],
            [9, -14],
            [7, -16],
            [6, -16],
        ],

        Ressources.SAUGE: [
            [6, -17],
            [5, -15],
            [2, -15],
            [3, -13],
            [3, -12],
            [3, -11],
            [5, -10],
            [5, -11],
            [5, -12],
            [5, -13],
            [5, -12],
            [7, -11],
            [7, -12],
            [7, -11],
            [8, -12],
            [9, -12],
            [9, -11],
            [9, -13],
            [9, -13],
            [10, -13],
            [10, -12],
            [10, -14],
            [7, -15],
        ],

        Ressources.TREFLE_A_5_FEUILLES: [
            [4, -15],
            [3, -11],
            [3, -10],
            [4, -11],
            [5, -11],
            [5, -10],
            [6, -10],
            [6, -9],
            [8, -10],
            [8, -14],
        ],
    }

    # IMAGES
    PHOENIX_STATUE_IMAGE: str = Images.PHOENIX_STATUE

    def get_path(self, from_location, to_location):
        """ get path from a position to another (add special locations to go to if there is obstacle in between) """
        path = []
        if Astrub.is_above_city(to_location) \
                and not Astrub.is_above_city(from_location) \
                and not Astrub.is_in_city(from_location) \
                and to_location[0] > Astrub.TOP_LEFT_CITY_CHECKPOINT[0] \
                and from_location[1] > Astrub.TOP_LEFT_CITY_CHECKPOINT[1]:
            path.append(Astrub.TOP_LEFT_CITY_CHECKPOINT)

        path.append(to_location)
        return path

    def get_aiming_location(self, from_location, to_location):
        if Astrub.is_in_city(to_location) or Astrub.is_in_city(from_location):
            return Astrub.get_aiming_location(from_location, to_location)

        if Astrub.is_above_city(to_location) \
                and not Astrub.is_above_city(from_location) \
                and not Astrub.is_in_city(from_location) \
                and to_location[0] > Astrub.TOP_LEFT_CITY_CHECKPOINT[0] \
                and from_location[1] > Astrub.TOP_LEFT_CITY_CHECKPOINT[1]:
            return Astrub.TOP_LEFT_CITY_CHECKPOINT

        if -19 >= from_location[1] >= -17 and from_location[0] == 2 and to_location[1] >= -16:
            return [2, -16]

        return to_location