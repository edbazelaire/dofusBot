from src.enum.regions import Regions


class Locations:
    """ map city """
    GATES_LOCATION = (4, -22)
    TOP_CORNER_CITY_LOCATION = [2, -22]

    ASTRUB_TOP_LEFT = [3, -19]
    ASTRUB_BOTTOM_RIGHT = [6, -17]

    BONTA_MILICE_LOCATION = [-32, -57]

    ZAAPS = {
        Regions.PLAINES_CANIA: [-27, -36]
    }

    PHOENIX_STATUES = {
        Regions.CHAMP_ASTRUB: [2, -14],
        Regions.PLAINES_CANIA: [-10, -54]
    }

    @staticmethod
    def is_above_astrub(pos):
        return pos[1] < Locations.ASTRUB_TOP_LEFT[1]

    @staticmethod
    def is_below_astrub(pos):
        return pos[1] > Locations.ASTRUB_BOTTOM_RIGHT[1]