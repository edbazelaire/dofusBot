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
    CHECKPOINT: list = Astrub.TOP_CITY_CHECKPOINT
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

            Ressources.FRENE: [
                [1, -18],
                [0, -18],
                [0, -17],
                [0, -16],
                [0, -15],
                [-1, -15],
                [-2, -15],
                [-3, -15],
                [-3, -16],
                [-2, -16],
                [-1, -16],
                [-1, -17],
                [-2, -17],
                [-3, -17],
                [-3, -18],
                [-3, -19],
                [-2, -19],
                [-2, -18],
                [-1, -18],
                [-1, -19],
                [0, -19],
                [1, -19],
                [0, -20],
                [-1, -20],
                [-2, -20],
                [-3, -20],
                [-3, -21],
                [-2, -21],
                [-1, -21],
                [0, -21],
                [-1, -21],
                [-2, -21],
                [-3, -21],
                [-3, -22],
                [-2, -22],
                [-1, -22],
                [0, -22],
                [1, -22],
                [2, -22],
                [2, -23],
                [1, -23],
                [0, -23],
                [-1, -23],
                [-2, -23],
                [-2, -23],
                [-2, -24],
                [-1, -24],
                [0, -24],
                [1, -24],
                [2, -24],
                [2, -25],
                [1, -25],
                [0, -25],
                [-1, -25],
                [-2, -25],
                [-2, -26],
                [-1, -26],
                [0, -26],
                [1, -26],
                [2, -26],
                [2, -27],
                [1, -27],
                [0, -27],
                [-1, -27],
                [-2, -27],
                [-2, -28],
                [-1, -28],
                [0, -28],
                [1, -28],
                [2, -28],
            ]
        }

    # IMAGES
    PHOENIX_STATUE_IMAGE: str = Images.get_screenshot(Images.PHOENIX_STATUE)

    def get_path(self, from_location, to_location):
        """ get path from a position to another (add special locations to go to if there is obstacle in between) """
        path = []
        if Astrub.is_above_city(to_location) \
                and not Astrub.is_in_city(from_location) \
                and from_location[1] > Astrub.TOP_LEFT_CITY_CHECKPOINT[1]:
            path.append(Astrub.TOP_LEFT_CITY_CHECKPOINT)

        path.append(to_location)
        return path