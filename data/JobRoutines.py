from enum import Enum

from src.enum.regions import Regions
from src.enum.ressources import Ressources
from src.utils.ErrorHandler import ErrorHandler


class CharNames(Enum):
    # TEAM 2
    PASCA_VIVIE = 'Pasca-Vivie'
    ALIC_CLARIA = 'Alic-Claria'
    INCE_ROLA = 'Ince-Rola'
    RALPHERTIN = 'Ralphertin'


class JobRoutine:
    def __init__(self, region_name, ressources, crafts, city_name=None):
        self.region_name = region_name
        self.ressources = ressources
        self.crafts = crafts
        self.city_name = city_name


def get_job_routine(char_name: (str, CharNames)) -> (None, JobRoutine):
    if isinstance(char_name, CharNames):
        char_name = char_name.value

    if char_name == CharNames.PASCA_VIVIE.value:
        return JobRoutine(
            region_name=Regions.CHAMP_ASTRUB,
            ressources=[Ressources.HOUBLON],
            crafts=[]
        )

    if char_name == CharNames.RALPHERTIN.value:
        return JobRoutine(
            region_name=Regions.CHAMP_ASTRUB,
            ressources=[Ressources.ORTIE, Ressources.SAUGE, Ressources.TREFLE_A_5_FEUILLES],
            crafts=[Ressources.POTION_DE_SOUVENIR]
        )

    if char_name == CharNames.INCE_ROLA.value:
        return JobRoutine(
            region_name=Regions.CHAMP_ASTRUB,
            ressources=[Ressources.FRENE, Ressources.CHATAIGNER, Ressources.NOYER],
            crafts=[]
        )

    if char_name == CharNames.ALIC_CLARIA.value:
        return JobRoutine(
            region_name=Regions.PRAIRIE_ASTRUB,
            ressources=[Ressources.ORTIE, Ressources.SAUGE],
            crafts=[Ressources.POTION_DE_SOUVENIR]
        )

    ErrorHandler.error(f'unable to find JobRoutine for {JobRoutine}')
    return None


def get_char_id(char_name: (str, CharNames)):
    if isinstance(char_name, CharNames):
        char_name = char_name.value

    if char_name == CharNames.PASCA_VIVIE.value:
        return '#5244'

    if char_name == CharNames.RALPHERTIN.value:
        return '#9961'

    if char_name == CharNames.INCE_ROLA.value:
        return '#6773'
