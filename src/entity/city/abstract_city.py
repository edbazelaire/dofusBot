class AbstractCity:
    REGION = ''
    SUB_REGION = ''

    BANK_LOCATION = []
    BANK_DOOR_POSITION = []
    GET_OUT_BANK_POSITION = []
    BANK_NPC_IMAGE = ''

    @staticmethod
    def is_in_city(location) -> bool:
        pass

    @staticmethod
    def get_path(from_location, to_location) -> list:
        pass

    @staticmethod
    def get_bank_path(location) -> list:
        pass
