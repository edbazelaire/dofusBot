from src.location_handling.city.astrub import Astrub
from src.location_handling.city.bonta import Bonta
from src.utils.ErrorHandler import ErrorHandler


class AbstractCity:
    """ static class that handles all the specific information of a city (bank location, zaap location, specific images, ...)"""

    NAME = ''                   # name of the city
    SUB_REGION = ''             # (unused) name of the city's sub-region in the map

    BANK_LOCATION = []          # location of the bank in the city
    BANK_DOOR_POSITION = []     # screen position (x, y) to click in order to get in the bank
    GET_OUT_BANK_POSITION = []  # screen position to click to get out the bank
    BANK_NPC_IMAGE = ''         # image of the NPC in the bank to talk to

    @staticmethod
    def get_city(city_name: str):
        """ get the city class from its name """
        if city_name == Bonta.NAME:
            return Bonta()
        elif city_name == Astrub.NAME:
            return Astrub()

        else:
            ErrorHandler.fatal_error("unknown city {city_name}")

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


