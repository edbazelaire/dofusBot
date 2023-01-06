from src.enum.images import Images
from src.location_handling.city.abstract_city import AbstractCity


class Frigost(AbstractCity):
    NAME = 'Frigost'                            # name of the city
    SUB_REGION = ''                             # (unused) name of the city's sub-region in the map

    BANK_LOCATION = [-77, -41]                  # location of the bank in the city
    ZAAP = [-78, -41]                           # location of the zaap in the city
    BANK_DOOR_POSITION = (1105, 458)            # screen position (x, y) to click in order to get in the bank
    GET_OUT_BANK_POSITION = (710, 704)          # screen position to click to get out the bank
    BANK_NPC_IMAGE = Images.BANK_NPC_ASTRUB     # image of the NPC in the bank to talk to

    CITY_TOP_LEFT = [-83, -46]
    CITY_BOTTOM_RIGHT = [-76, -32]

    TOP_CITY_CHECKPOINT = [-76, -46]

    @staticmethod
    def get_path(from_location, to_location):
        path = []
        # GOING OUT of the city
        if Frigost.is_in_city(from_location):
            if not Frigost.is_in_city(to_location):
                path.append(Frigost.TOP_CITY_CHECKPOINT)
                path.append([Frigost.TOP_CITY_CHECKPOINT[0], Frigost.TOP_CITY_CHECKPOINT[1] - 1])

        # GOING IN the city
        elif Frigost.is_in_city(to_location):
            if not Frigost.is_in_city(from_location):
                if from_location[1] > -46:
                    path.append([-70, -46])
                path.append(Frigost.TOP_CITY_CHECKPOINT)

        path.append(to_location)
        return path

    @staticmethod
    def get_bank_path(location) -> list:
        """ find path to the bank from anywhere
        :param location: location of the player
        :return: list of positions to go to in order to get to the bank
        """
        return Frigost.get_path(location, Frigost.BANK_LOCATION)

    @staticmethod
    def is_in_city(location):
        return Frigost.CITY_BOTTOM_RIGHT[0] >= location[0] >= Frigost.CITY_TOP_LEFT[0] \
            and Frigost.CITY_BOTTOM_RIGHT[1] >= location[1] >= Frigost.CITY_TOP_LEFT[1]
