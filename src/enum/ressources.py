import enum

from src.utils.ErrorHandler import ErrorHandler


class Ressources:
    """ ressources names """
    # ==================================================================================================================
    # COLLECTABLES
    # CEREALS
    HOUBLON = "houblon"
    BLE = "ble"
    ORGES = "orges"
    SEIGLE = "seigle"
    CHANVRE = "chanvre"
    MALT = "malt"

    # WOOD
    FRENE = 'frene'
    CHATAIGNER = 'chataigner'

    # METALS
    FER = 'fer'

    # ==================================================================================================================
    # CRAFTS
    BRIOCHETTE = 'briochette'
    PAIN_AMAKNA = 'pain d\'amakna'

    # ==================================================================================================================
    # OTHERS
    TREFLES = 'trefles'
    CENDRES_ETERNELLES = 'cendres_eternelles'

    @staticmethod
    def get(ressource_name):
        # ==============================================================================================================
        # COLLECTABLES
        if ressource_name == Ressources.HOUBLON:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=2
            )

        elif ressource_name == Ressources.CENDRES_ETERNELLES:
            return RessourceConfig(
                name='cendres éternelles',
                ressource_type=RessourceType.Ressource,
                pods=1
            )

        elif ressource_name == Ressources.TREFLES:
            return RessourceConfig(
                name='trefle à 5 feuilles',
                ressource_type=RessourceType.Ressource,
                pods=1
            )

        # ==============================================================================================================
        # CRAFTS
        elif ressource_name == Ressources.BRIOCHETTE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Consumable,
                pods=2
            )

        elif ressource_name == Ressources.PAIN_AMAKNA:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Consumable,
                pods=2
            )

        # ==============================================================================================================
        else:
            ErrorHandler.fatal_error(f'unknown ressource config for ressource {ressource_name}')


class RessourceType(enum.Enum):
    All = 0
    Item = 1
    Consumable = 2
    Ressource = 3
    Cosmetic = 4


class RessourceConfig:
    def __init__(self, name, ressource_type, pods):
        self.name = name
        self.type = ressource_type
        self.pods = pods

        # SELLING CONFIG
        # self.sell_order = sell_order        # number of ressources in the hdv


