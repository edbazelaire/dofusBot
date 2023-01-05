from src.buildings.Bank import Bank
from src.location_handling.city.abstract_city import AbstractCity
from src.enum.actions import Actions
from src.enum.images import Images


class Bonta(AbstractCity):
    NAME = 'Bonta'
    SUB_REGION = ''

    CITY_TOP_CORNER = [-37, -61]
    CITY_BOTTOM_CORNER = [-26, -50]

    BANK_LOCATION = [-31, -57]

    def __init__(self):
        super().__init__()

        self.bank = Bank(
            location=self.BANK_LOCATION,
            door_position=(964, 677),
            exit_position=(519, 798),
            npc_image=Images.BANK_NPC_BONTA
        )

    @staticmethod
    def is_in_city(location):
        return Bonta.CITY_BOTTOM_CORNER[0] >= location[0] >= Bonta.CITY_TOP_CORNER[0] \
            and Bonta.CITY_BOTTOM_CORNER[1] >= location[1] >= Bonta.CITY_TOP_CORNER[1]

    @staticmethod
    def get_aiming_location(from_location, to_location):
        """ next location to go to in order to be able to go to requested location """
        if Bonta.is_in_city(from_location) and not Bonta.is_in_city(to_location):
            return Actions.TAKE_RECALL_POTION

        elif Bonta.is_in_city(to_location) and not Bonta.is_in_city(from_location):
            return Actions.TAKE_BONTA_POTION

        return to_location
