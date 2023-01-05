from src.buildings.Bank import Bank
from src.buildings.craft_building import CraftBuilding


class AbstractCity:
    """ static class that handles all the specific information of a city (bank location, zaap location, specific images, ...)"""

    NAME = ''                   # name of the city
    SUB_REGION = ''             # (unused) name of the city's sub-region in the map
    RESIZED = False             # has been resized already

    bank: Bank

    def __init__(self):
        if not self.RESIZED:
            self.RESIZED = True

    @staticmethod
    def is_in_city(location) -> bool:
        """ check if location is in the city """
        pass

    @staticmethod
    def get_aiming_location(from_location, to_location) -> list:
        """ next location to go to in order to be able to go to requested location """
        pass

    @staticmethod
    def get_craft_building(job) -> CraftBuilding:
        """ get path to the bank from anywhere in the global map """
        pass


