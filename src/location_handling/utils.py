from src.location_handling.city.Frigost import Frigost
from src.location_handling.city.astrub import Astrub
from src.location_handling.city.bonta import Bonta
from src.location_handling.regions.mine_astrub import MineAstrub
from src.location_handling.regions.champ_astrub import ChampAstrub
from src.location_handling.regions.champ_glace import ChampGlace
from src.location_handling.regions.planies_cania import PlainesCania
from src.utils.ErrorHandler import ErrorHandler


def get_city(city_name: str):
    """ get the city class from its name """
    if city_name == Bonta.NAME:
        return Bonta()
    elif city_name == Astrub.NAME:
        return Astrub()
    elif city_name == Frigost.NAME:
        return Frigost()

    else:
        ErrorHandler.fatal_error(f"unknown city {city_name}")


def get_region(region_name: str, ressources: list):
    if region_name == PlainesCania.NAME:
        return PlainesCania(ressources)
    elif region_name == ChampAstrub.NAME:
        return ChampAstrub(ressources)
    elif region_name == MineAstrub.NAME:
        return MineAstrub(ressources)
    elif region_name == ChampGlace.NAME:
        return ChampGlace(ressources)
    else:
        ErrorHandler.fatal_error(f"unknown region {region_name}")