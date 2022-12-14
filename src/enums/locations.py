class Locations:
    """ map locations """
    DEATH_MAP_LOCATION = (6, -19)
    BANK_LOCATION = (4, -18)
    GATES_LOCATION = (4, -22)
    TOP_CORNER_CITY_LOCATION = [2, -22]
    PHOENIX_STATUE = [2, -14]

    ASTRUB_TOP_LEFT = [3, -19]
    ASTRUB_BOTTOM_RIGHT = [6, -17]

    @staticmethod
    def is_in_astrub(pos):
        return Locations.ASTRUB_BOTTOM_RIGHT[0] >= pos[0] >= Locations.ASTRUB_TOP_LEFT[0] \
            and Locations.ASTRUB_BOTTOM_RIGHT[1] >= pos[1] >= Locations.ASTRUB_TOP_LEFT[1]

    @staticmethod
    def is_above_astrub(pos):
        return pos[1] < Locations.ASTRUB_TOP_LEFT[1]

    @staticmethod
    def is_below_astrub(pos):
        return pos[1] > Locations.ASTRUB_BOTTOM_RIGHT[1]