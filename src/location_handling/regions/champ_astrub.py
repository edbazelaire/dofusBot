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
        # CEREALS
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
        Ressources.ORGES: [
            [5, -22],
            [4, -23],
            [3, -24],
            [3, -26],
            [3, -28],
            [3, -31],
            [4, -30],
            [5, -30],
            [6, -29],
            [5, -27],
            [7, -27],
            [7, -24],
            [8, -24],
            [6, -24],
            [6, -22],
        ],
        Ressources.AVOINE: [
            [3, -22],
            [3, -24],
            [3, -26],
            [3, -31],
            [4, -28],
            [6, -25],
            [9, -24],
            [7, -21],
            [6, -22],
        ],
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

        # WOOD
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
        ],
        Ressources.CHATAIGNER: [
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
        ],
        Ressources.NOYER: [
            [1, -18],
            [0, -15],
            [-1, -15],
            [-2, -15],
            [-3, -15],
            [-3, -16],
            [-1, -16],
            [-2, -17],
            [-3, -18],
            [-3, -19],
            [-3, -20],
            [-3, -21],
            [-3, -22],
            [-2, -23],
            [-2, -24],
            [-1, -24],
            [0, -24],
            [2, -24],
            [2, -25],
            [1, -25],
            [-2, -25],
            [-2, -26],
            [-2, -27],
            [-2, -28]
        ],
        Ressources.CHENE: [
            [0, -22],
            [0, -23],
            [1, -23],
            [2, -23],
            [2, -24],
            [0, -24],
            [-1, -24],
            [-1, -25],
            [-2, -25],
            [1, -26],
            [1, -27],
            [1, -28],
        ],
        Ressources.BOMBU: [
            [-6, -19],
            [-7, -19],
            [-8, -19],
            [-8, -20],
            [-7, -20],
            [-7, -21],
            [-7, -22],
            [-7, -23],
            [-8, -23],
            [-7, -24],
            [-7, -25],
            [-8, -25],
            [-8, -26],
            [-7, -26],
            [-7, -27],
            [-7, -28],
            [-8, -28],
            [-8, -29],
            [-7, -29],
            [-7, -30],
            [-8, -30],
            [-6, -30],
            [-6, -31],
            [-6, -32],
            [-6, -33],
            [-7, -32],
            [-8, -32],
            [-8, -31],
            [-9, -31],
            [-8, -33],
            [-9, -33],
            [-9, -34],
            [-10, -34],
            [-10, -33],
            [-11, -33],
            [-11, -32],
            [-11, -31],
            [-11, -30],
            [-12, -33],
            [-12, -34],
            [-12, -35],
            [-12, -36],
            [-11, -36],
            [-10, -36],
            [-9, -36],
            [-13, -36],
            [-13, -35],
            [-14, -35],
            [-15, -35],
            [-16, -35],
            [-16, -36],
            [-15, -36],
            [-14, -37],
            [-14, -38],
            [-15, -38],
            [-15, -39],
            [-15, -40],
            [-15, -41],
            [-16, -42],
            [-16, -41],
            [-17, -42],
            [-17, -43],
            [-18, -42],
            [-18, -41],
            [-19, -40],
            [-20, -39],
            [-20, -38],
            [-20, -36],
            [-19, -36],
            [-19, -37],
            [-18, -36],
        ],
        Ressources.ERABLE: [
            [-1, -21],
            [-1, -22],
            [0, -21],
            [1, -21],
            [1, -20],
            [1, -19],
            [0, -19],
            [-1, -19],
            [1, -18],
            [1, -17],
            [1, -15],
            [2, -15],
            [3, -15],
            [4, -15],
            # [6, -15],
            # [6, -16],
            # [7, -16],
            # [7, -17],
        ],
        Ressources.IF: [
            [-1, -17],
            [-2, -17],
            [-2, -16],
            [-2, -15],
            [-3, -15],
            [-2, -18],
            [-2, -19],
            [-2, -20],
            [-3, -21],
        ],

        # PLANTS
        Ressources.ORTIE: [
            [4, -19],
            [3, -20],
            [2, -21],
            [2, -22],
            [1, -22],
            [1, -23],
            [2, -23],
            [2, -24],
            [1, -24],
            [2, -25],
            [3, -25],
            [2, -26],
            [2, -27],
            [2, -28],
            [2, -29],
            [2, -30],
            [3, -30],
            [3, -31],
            [4, -31],
            [4, -30],
            [4, -29],
            [3, -29],
            [3, -28],
            [4, -28],
            [5, -29],
            [5, -30],
            [6, -30],
            [6, -29],
            [6, -28],
            [6, -26],
            [7, -25],
            [7, -22],
            [7, -20],
            [6, -21],
            [5, -20],
        ],
        Ressources.SAUGE: [
            [-3, -19],
            [-3, -20],
            # [4, -20],
            [-3, -21],
            [-2, -21],
            [-2, -22],
            [-2, -23],
            [-2, -24],
            # [-3, -24],
            # [-4, -24],
            [-1, -24],
            [0, -24],
            [1, -24],
            [1, -25],
            [1, -26],
            [0, -26],
            [-1, -26],
            [-1, -27],
            [0, -27],
            [1, -27],
            [1, -28],
            [3, -31],
            [3, -32],
            [4, -32],
            [5, -30],
            [5, -29],
            [5, -27],
            [6, -27],
            [7, -28],
            [6, -24],
            [7, -23],
            [8, -23],
            [9, -23],
            [5, -22],
        ],
        Ressources.TREFLE_A_5_FEUILLES: [
            [0, -18],
            [0, -17],
            [0, -16],
            [0, -15],
            [-1, -15],
            [-1, -16],
            [-2, -16],
            [-3, -16],
            [-3, -17],
            [-1, -17],
            [-1, -18],
            [-2, -18],
            [-3, -18],
            [-3, -19],
            [-2, -19],
            [-1, -19],
            [-1, -20],
            [-3, -20],
            [-3, -21],
            [-3, -22],
            [-2, -21],
            [-1, -21],
            [0, -21],
            [0, -22],
            [0, -23],
            [2, -23],
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

        if from_location == [4, -32] and to_location[0] >= 5:
            return [4, -31]

        if from_location == [5, -31] and to_location[0] >= 6:
            return [5, -30]

        if from_location[0] == 6 and -29 >= from_location[1] >= -30 and to_location[0] >= 7:
            return [6, -28]

        if from_location[0] == 7 and -25 >= from_location[1] >= -28 and to_location[0] >= 8:
            return [7, -24]

        return to_location