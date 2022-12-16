from src.enum.regions import Regions
from src.enum.ressources import Ressources


class Locations:
    """ map locations """
    DEATH_MAP_LOCATION = (6, -19)
    BANK_LOCATION = (4, -18)
    GATES_LOCATION = (4, -22)
    TOP_CORNER_CITY_LOCATION = [2, -22]
    PHOENIX_STATUE = [2, -14]

    ASTRUB_TOP_LEFT = [3, -19]
    ASTRUB_BOTTOM_RIGHT = [6, -17]

    RESSOURCES_LOCATIONS = {
        Regions.CHAMP_ASTRUB: {
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
        },

        Regions.PLAINES_CANIA: {
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

            "fake": []
        }
    }

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