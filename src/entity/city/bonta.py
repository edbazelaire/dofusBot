from src.entity.city.abstract_city import AbstractCity
from src.entity.city.astrub import Astrub
from src.utils.utils_fct import read_region


class Bonta(AbstractCity):
    REGION = 'Bonta'
    SUB_REGION = ''             # TODO

    BANK_LOCATION = ''          # TODO

    @staticmethod
    def get_bank_path(location) -> list:
        """ find path to the bank from anywhere
        :param location: location of the player
        :return: list of positions to go to in order to get to the bank
        """
        path = []
        if not Bonta.is_in_city(location):
            path.append(AbstractCity.TAKE_POTION_BONTA)

        path.append(Bonta.BANK_LOCATION)

        return path

    @staticmethod
    # TODO -----------------------------------
    def is_in_city(location):
        region, sub_region = read_region()

    @staticmethod
    def is_above_city(location):
        return location[1] < Astrub.ASTRUB_TOP_LEFT[1]

    @staticmethod
    def is_below_city(location):
        return location[1] > Astrub.ASTRUB_BOTTOM_RIGHT[1]