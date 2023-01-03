from src.buildings.Bank import Bank
from src.buildings.abstract_building import AbstractBuilding
from src.buildings.craft_building import CraftBuilding
from src.enum.positions import Positions


class AbstractCity:
    """ static class that handles all the specific information of a city (bank location, zaap location, specific images, ...)"""

    NAME = ''                   # name of the city
    SUB_REGION = ''             # (unused) name of the city's sub-region in the map
    RESIZED = False             # has been resized already

    bank: Bank

    def __init__(self):
        if not self.RESIZED:
            self.BANK_DOOR_POSITION = Positions.resize(self.BANK_DOOR_POSITION)
            self.GET_OUT_BANK_POSITION = Positions.resize(self.GET_OUT_BANK_POSITION)

            self.RESIZED = True

    @staticmethod
    def is_in_city(location) -> bool:
        """ check if location is in the city """
        pass

    @staticmethod
    def get_path(from_location, to_location) -> list:
        """ get path from a location to another if at least one of theme is in the city """
        pass

    @staticmethod
    def get_bank_path(location) -> list:
        """ get path to the bank from anywhere in the global map """
        pass

    @staticmethod
    def get_craft_building(job) -> CraftBuilding:
        """ get path to the bank from anywhere in the global map """
        pass


