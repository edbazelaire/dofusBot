from src.buildings.Bank import Bank
from src.location_handling.city.abstract_city import AbstractCity
from src.enum.images import Images


class Astrub(AbstractCity):
    NAME = 'Astrub'
    SUB_REGION = ''

    TOP_CITY_CHECKPOINT = [4, -22]
    BOTTOM_CITY_CHECKPOINT = [5, -17]
    LEFT_CITY_CHECKPOINT = [2, -17]
    TOP_LEFT_CITY_CHECKPOINT = [2, -22]

    ASTRUB_TOP_LEFT = [3, -19]
    ASTRUB_BOTTOM_RIGHT = [6, -17]

    bank = Bank(
        bank_location=[4, -18],
        bank_door_position=[1138, 372],
        bank_npc_image=Images.BANK_NPC_ASTRUB,
        get_out_bank_position=[735, 710]
    )

    @staticmethod
    def get_path(from_location, to_location):
        path = []
        # GOING OUT of the city
        if Astrub.is_in_city(from_location):
            if Astrub.is_above_city(to_location):
                path.append(Astrub.TOP_CITY_CHECKPOINT)
            elif Astrub.is_left_city(to_location):
                path.append(Astrub.LEFT_CITY_CHECKPOINT)
                path.append(Astrub.LEFT_CITY_CHECKPOINT + [-1, 0])
            elif Astrub.is_below_city(to_location):
                path.append(Astrub.BOTTOM_CITY_CHECKPOINT)
                path.append(Astrub.BOTTOM_CITY_CHECKPOINT + [0, 1])

        # GOING IN the city
        elif Astrub.is_in_city(to_location):
            if Astrub.is_above_city(from_location):
                path.append(Astrub.TOP_CITY_CHECKPOINT)

            elif Astrub.is_left_city(from_location):
                path.append(Astrub.LEFT_CITY_CHECKPOINT + [-1, 0])
                path.append(Astrub.LEFT_CITY_CHECKPOINT)

            elif Astrub.is_below_city(from_location):
                path.append(Astrub.BOTTOM_CITY_CHECKPOINT + [0, 1])
                path.append(Astrub.BOTTOM_CITY_CHECKPOINT)

        path.append(to_location)
        return path

    @staticmethod
    def get_bank_path(location) -> list:
        """ find path to the bank from anywhere
        :param location: location of the player
        :return: list of positions to go to in order to get to the bank
        """
        return Astrub.get_path(location, Astrub.bank.BANK_LOCATION)

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

    @staticmethod
    def is_left_city(location):
        return location[0] < Astrub.ASTRUB_TOP_LEFT[0]