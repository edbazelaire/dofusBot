from src.entity.city.abstract_city import AbstractCity


class Astrub(AbstractCity):
    REGION = 'Astrub'
    SUB_REGION = ''             # TODO

    BANK_LOCATION = [4, -18]
    TOP_CITY_CHECKPOINT = [4, -22]
    TOP_LEFT_CITY_CHECKPOINT = [2, -22]

    ASTRUB_TOP_LEFT = [3, -19]
    ASTRUB_BOTTOM_RIGHT = [6, -17]

    @staticmethod
    def get_bank_path(location) -> list:
        """ find path to the bank from anywhere
        :param location: location of the player
        :return: list of positions to go to in order to get to the bank
        """
        path = []
        if Astrub.is_above_city(location):
            path.append(Astrub.TOP_CITY_CHECKPOINT)

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