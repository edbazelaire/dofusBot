import enum

from src.utils.ErrorHandler import ErrorHandler


class Ressources:
    """ ressources names """
    # ==================================================================================================================
    # COLLECTABLES
    # CEREALS
    BLE = "ble"
    ORGES = "orges"
    AVOINE = "avoine"
    HOUBLON = "houblon"
    SEIGLE = "seigle"
    CHANVRE = "chanvre"
    MALT = "malt"
    FROSTIZ = "frostiz"

    # WOOD
    FRENE = 'frene'
    CHATAIGNER = 'chataigner'
    NOYER = 'noyer'
    CHENE = 'chene'
    BOMBU = 'bombu'
    ERABLE = 'erable'
    IF = 'if'

    # PLANTS
    ORTIE = 'ortie'
    SAUGE = 'sauge'
    TREFLE_A_5_FEUILLES = 'trefle a 5 feuilles'
    ORCHIDEE_FREYESQUE = 'orchidee freyesque'

    # METALS
    FER = 'fer'

    # ==================================================================================================================
    # CRAFTS
    PAIN_D_INCARNAM = 'pain d\'incarnam'
    CARASAU = 'carasau'
    PAIN_AUX_FLOCONS_D_AVOINE = 'pain aux flocons d\'avoine'
    BRIOCHETTE = 'briochette'
    PAIN_DE_SEIGLE = 'pain de seigle'
    POTION_DE_SOUVENIR = 'potion de souvenir'
    PLANCHE_DE_SURF = 'planche de surf'
    SUBSTRAT_DE_FUTAIE = 'substrat de futaie'

    # ==================================================================================================================
    # OTHERS
    CENDRES_ETERNELLES = 'cendres eternelles'
    AUBERGINE = 'aubergine'
    EAU_POTABLE = 'eau potable'

    @staticmethod
    def get(ressource_name):
        # ==============================================================================================================
        # COLLECTABLES
        # -----------------------------------------------------------------------------------------
        # CEREALS
        if ressource_name == Ressources.BLE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=2
            )

        elif ressource_name == Ressources.ORGES:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=2
            )

        elif ressource_name == Ressources.AVOINE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=2
            )

        if ressource_name == Ressources.HOUBLON:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=2
            )

        if ressource_name == Ressources.SEIGLE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=2
            )

        # -----------------------------------------------------------------------------------------
        # CEREALS
        elif ressource_name == Ressources.FRENE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=5
            )
        elif ressource_name == Ressources.CHATAIGNER:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=5
            )
        elif ressource_name == Ressources.NOYER:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=5
            )
        elif ressource_name == Ressources.CHENE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=5
            )

        # -----------------------------------------------------------------------------------------
        # PLANTS
        elif ressource_name == Ressources.ORTIE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=1
            )

        elif ressource_name == Ressources.SAUGE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=1
            )

        elif ressource_name == Ressources.TREFLE_A_5_FEUILLES:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=1
            )

        elif ressource_name == Ressources.ORCHIDEE_FREYESQUE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=1
            )

        # -----------------------------------------------------------------------------------------
        # OTHER
        elif ressource_name == Ressources.CENDRES_ETERNELLES:
            return RessourceConfig(
                name='cendres eternelles',
                ressource_type=RessourceType.Ressource,
                pods=1
            )
        elif ressource_name == Ressources.AUBERGINE:
            return RessourceConfig(
                name='aubergine',
                ressource_type=RessourceType.Ressource,
                pods=1
            )
        elif ressource_name == Ressources.EAU_POTABLE:
            return RessourceConfig(
                name='aubergine',
                ressource_type=RessourceType.Ressource,
                pods=1
            )

        # ==============================================================================================================
        # CRAFTS
        # ------------------------------------------------
        # PAYSAN
        elif ressource_name == Ressources.PAIN_D_INCARNAM:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Consumable,
                pods=2
            )

        elif ressource_name == Ressources.CARASAU:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Consumable,
                pods=2
            )

        elif ressource_name == Ressources.PAIN_AUX_FLOCONS_D_AVOINE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Consumable,
                pods=2
            )

        elif ressource_name == Ressources.BRIOCHETTE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Consumable,
                pods=2
            )

        elif ressource_name == Ressources.PAIN_DE_SEIGLE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Consumable,
                pods=2
            )

        # ------------------------------------------------
        # BUCHERON
        elif ressource_name == Ressources.PLANCHE_DE_SURF:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=10
            )

        elif ressource_name == Ressources.SUBSTRAT_DE_FUTAIE:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
                pods=10
            )

        # ------------------------------------------------
        # ALCHIMIST
        elif ressource_name == Ressources.POTION_DE_SOUVENIR:
            return RessourceConfig(
                name=ressource_name,
                ressource_type=RessourceType.Ressource,
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


