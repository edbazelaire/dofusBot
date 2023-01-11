from enum import Enum

from src.enum.regions import Regions
from src.enum.ressources import Ressources
from src.utils.ErrorHandler import ErrorHandler


class CharNames(Enum):
    # TEAM 1
    PASCA_VIVIE     = 'Pasca-Vivie'
    ALIC_CLARIA     = 'Alic-Claria'
    INCE_ROLA       = 'Ince-Rola'
    RALPHERTIN      = 'Ralphertin'

    # TEAM 3
    Anabarch        = 'Anabarch'
    Borias          = 'Borias'
    Chouaoua        = 'Chouaoua'
    DinoFury        = 'DinoFury'

    # TEAM 4
    Azxcine	        = 'Azxcine'
    Bouyazine       = 'Bouyazine'
    Cinistropyia    = 'Cinistropyia'
    Doliphragie     = 'Doliphragie'


class JobRoutine:
    def __init__(self, region_name, ressources, crafts, city_name=None):
        self.region_name = region_name
        self.ressources = ressources
        self.crafts = crafts
        self.city_name = city_name


def get_job_routine(char_name: (str, CharNames)) -> (None, JobRoutine):
    if isinstance(char_name, CharNames):
        char_name = char_name.value

    # =========================================================================================
    # TEAM 1
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

    # =========================================================================================
    # TEAM 3
    if char_name == CharNames.Anabarch.value:
        return JobRoutine(
            region_name=Regions.CHAMP_ASTRUB,
            ressources=[Ressources.BLE],
            crafts=[Ressources.PAIN_D_INCARNAM]
        )

    if char_name == CharNames.Borias.value:
        return JobRoutine(
            region_name=Regions.CHAMP_ASTRUB,
            ressources=[Ressources.ORTIE],
            crafts=[]
        )

    if char_name == CharNames.Cinistropyia.value:
        return JobRoutine(
            region_name=Regions.CHAMP_ASTRUB,
            ressources=[Ressources.FRENE],
            crafts=[]
        )

    if char_name == CharNames.DinoFury.value:
        return JobRoutine(
            region_name=Regions.PRAIRIE_ASTRUB,
            ressources=[Ressources.ORTIE],
            crafts=[]
        )

    # =========================================================================================
    # TEAM 4

    if char_name == CharNames.Azxcine.value:
        return JobRoutine(
            region_name=Regions.CHAMP_ASTRUB,
            ressources=[Ressources.BLE],
            crafts=[Ressources.PAIN_D_INCARNAM]
        )

    if char_name == CharNames.Bouyazine.value:
        return JobRoutine(
            region_name=Regions.CHAMP_ASTRUB,
            ressources=[Ressources.ORTIE],
            crafts=[]
        )

    if char_name == CharNames.Chouaoua.value:
        return JobRoutine(
            region_name=Regions.CHAMP_ASTRUB,
            ressources=[Ressources.FRENE],
            crafts=[]
        )

    if char_name == CharNames.Doliphragie.value:
        return JobRoutine(
            region_name=Regions.PRAIRIE_ASTRUB,
            ressources=[Ressources.ORTIE],
            crafts=[]
        )

    ErrorHandler.error(f'unable to find JobRoutine for {JobRoutine}')
    return None

def get_char_id(char_name: (str, CharNames)):
    if isinstance(char_name, CharNames):
        char_name = char_name.value

    # TEAM 1 =====================================================
    if char_name == CharNames.PASCA_VIVIE.value:
        return '#5244'

    if char_name == CharNames.RALPHERTIN.value:
        return '#9961'

    if char_name == CharNames.INCE_ROLA.value:
        return '#6773'

    # TEAM 3 =====================================================
    if char_name == CharNames.Anabarch.value:
        return '#9443'

    if char_name == CharNames.Borias.value:
        return '#7676'

    if char_name == CharNames.Chouaoua.value:
        return '#5427'

    if char_name == CharNames.DinoFury.value:
        return '#6370'

    # TEAM 4 =====================================================
    if char_name == CharNames.Azxcine.value:
        return '#3953'

    if char_name == CharNames.Bouyazine.value:
        return '#7323'

    if char_name == CharNames.Cinistropyia.value:
        return '#6393'

    if char_name == CharNames.Doliphragie.value:
        return '#6357'