from src.buildings.Bank import Bank
from src.location_handling.city.abstract_city import AbstractCity
from src.location_handling.city.astrub import Astrub
from src.enum.actions import Actions
from src.enum.images import Images
from src.utils.utils_fct import read_region


class Bonta(AbstractCity):
    NAME = 'Bonta'
    SUB_REGION = ''

    CITY_TOP_CORNER = [-37, -61]
    CITY_BOTTOM_CORNER = [-26, -50]

    bank = Bank(
        bank_location=[-31, -57],
        bank_door_position=(964, 677),
        bank_npc_image=Images.BANK_NPC_BONTA,
        get_out_bank_position=(519, 798)
    )

    @staticmethod
    def get_bank_path(location) -> list:
        """ find path to the bank from anywhere
        :param location: location of the player
        :return: list of positions to go to in order to get to the bank
        """
        path = []
        if not Bonta.is_in_city(location):
            path.append(Actions.TAKE_BONTA_POTION)

        path.append(Bonta.bank.BANK_LOCATION)

        return path

    @staticmethod
    def is_in_city(location):
        return Bonta.CITY_BOTTOM_CORNER[0] >= location[0] >= Bonta.CITY_TOP_CORNER[0] \
            and Bonta.CITY_BOTTOM_CORNER[1] >= location[1] >= Bonta.CITY_TOP_CORNER[1]

    @staticmethod
    def get_path(from_location, to_location):
        path = []
        if Bonta.is_in_city(from_location) and not Bonta.is_in_city(to_location):
            path.append(Actions.TAKE_RECALL_POTION)

        elif Bonta.is_in_city(to_location) and not Bonta.is_in_city(from_location):
            path.append(Actions.TAKE_BONTA_POTION)

        path.append(to_location)
        return path
