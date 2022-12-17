from src.entity.city.abstract_city import AbstractCity
from src.enum.images import Images


class Astrub(AbstractCity):
    REGION = 'Astrub'
    SUB_REGION = ''

    BANK_LOCATION = [4, -18]
    BANK_DOOR_POSITION = [1138, 372]
    BANK_NPC_IMAGE = Images.get_bank(Images.BANK_NPC_ASTRUB)
    GET_OUT_BANK_POSITION = [735, 710]

    TOP_CITY_CHECKPOINT = [4, -22]
    BOTTOM_CITY_CHECKPOINT = [5, -17]
    TOP_LEFT_CITY_CHECKPOINT = [2, -22]

    ASTRUB_TOP_LEFT = [3, -19]
    ASTRUB_BOTTOM_RIGHT = [6, -17]

    @staticmethod
    def get_path(from_location, to_location):
        path = []
        if Astrub.is_in_city(from_location):
            if Astrub.is_above_city(to_location):
                path.append(Astrub.TOP_CITY_CHECKPOINT)
            elif Astrub.is_below_city(to_location):
                path.append(Astrub.BOTTOM_CITY_CHECKPOINT)

        elif Astrub.is_above_city(from_location) and Astrub.is_in_city(to_location):
            path.append(Astrub.TOP_CITY_CHECKPOINT)

        elif Astrub.is_below_city(from_location) and Astrub.is_in_city(to_location):
            path.append(Astrub.BOTTOM_CITY_CHECKPOINT)

        path.append(to_location)
        return path

    @staticmethod
    def get_bank_path(location) -> list:
        """ find path to the bank from anywhere
        :param location: location of the player
        :return: list of positions to go to in order to get to the bank
        """
        path = []
        if Astrub.is_above_city(location):
            path.append(Astrub.TOP_CITY_CHECKPOINT)
        if Astrub.is_below_city(location):
            path.append(Astrub.BOTTOM_CITY_CHECKPOINT)

        path.append(Astrub.BANK_LOCATION)

        return path

    @staticmethod
    def is_in_city(location):
        return Astrub.ASTRUB_BOTTOM_RIGHT[0] >= location[0] >= Astrub.ASTRUB_TOP_LEFT[0] \
               and Astrub.ASTRUB_BOTTOM_RIGHT[1] >= location[1] >= Astrub.ASTRUB_TOP_LEFT[1]

    @staticmethod
    def is_above_city(location):
        return location[1] < Astrub.ASTRUB_TOP_LEFT[1]

    @staticmethod
    def is_below_city(location):
        return location[1] > Astrub.ASTRUB_BOTTOM_RIGHT[1]