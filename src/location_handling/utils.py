from src.enum.regions import Regions
from src.location_handling.city.astrub import Astrub
from src.location_handling.city.bonta import Bonta
from src.location_handling.regions.champ_astrub import ChampAstrub
from src.location_handling.regions.planies_cania import PlainesCania
from src.utils.ErrorHandler import ErrorHandler


def get_city(city_name: str):
    """ get the city class from its name """
    if city_name == Bonta.NAME:
        return Bonta()
    elif city_name == Astrub.NAME:
        return Astrub()

    else:
        ErrorHandler.fatal_error("unknown city {city_name}")


def get_region(region_name: str, ressources: list):
    if region_name == Regions.PLAINES_CANIA:
        return PlainesCania(ressources)
    elif region_name == Regions.CHAMP_ASTRUB:
        return ChampAstrub(ressources)
    else:
        ErrorHandler.fatal_error(f"unknown region {region_name}")