from src.buildings.Bank import Bank
from src.enum.images import Images
from src.location_handling.city.abstract_city import AbstractCity
from src.utils.utils_fct import in_between_loc


class VillageDesEleveurs(AbstractCity):
    NAME = 'village des eleveurs'

    CITY_TOP_CORNER = [-18, -1]
    CITY_BOTTOM_CORNER = [-15, 5]

    BANK_LOCATION = [-16, 4]

    def __init__(self):
        super().__init__()

        self.bank = Bank(
            location=self.BANK_LOCATION,
            door_position=(1105, 461),
            exit_position=(802, 709),
            npc_image=Images.BANK_NPC_ASTRUB
        )

    @staticmethod
    def is_in_city(location):
        return in_between_loc(location, VillageDesEleveurs.CITY_TOP_CORNER, VillageDesEleveurs.CITY_BOTTOM_CORNER)

    @staticmethod
    def get_aiming_location(from_location, to_location):
        return to_location
