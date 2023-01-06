from src.buildings.Bank import Bank
from src.buildings.craft_building import CraftBuilding
from src.enum.jobs import Jobs
from src.location_handling.city.abstract_city import AbstractCity
from src.enum.images import Images
from src.utils.ErrorHandler import ErrorHandler


class Astrub(AbstractCity):
    NAME = 'Astrub'
    SUB_REGION = ''

    TOP_CITY_CHECKPOINT = [4, -20]
    BOTTOM_CITY_CHECKPOINT = [5, -17]
    LEFT_CITY_CHECKPOINT = [3, -18]
    TOP_LEFT_CITY_CHECKPOINT = [2, -20]

    ASTRUB_TOP_LEFT = [3, -19]
    ASTRUB_BOTTOM_RIGHT = [6, -17]

    BANK_LOCATION = [4, -18]

    def __init__(self):
        super().__init__()

        self.bank = Bank(
            location=self.BANK_LOCATION,
            door_position=(1138, 372),
            npc_image=Images.BANK_NPC_ASTRUB,
            exit_position=(735, 710)
        )

    @staticmethod
    def get_aiming_location(from_location, to_location):
        # MOVING INSIDE THE CITY
        if Astrub.is_in_city(from_location) and Astrub.is_in_city(to_location):
            return to_location

        # GOING OUT of the city
        elif Astrub.is_in_city(from_location):
            if Astrub.is_above_city(to_location):
                if from_location == Astrub.TOP_CITY_CHECKPOINT:
                    return [Astrub.TOP_CITY_CHECKPOINT[0], Astrub.TOP_CITY_CHECKPOINT[1] - 1]
                return Astrub.TOP_CITY_CHECKPOINT

            elif Astrub.is_left_city(to_location):
                if from_location == Astrub.LEFT_CITY_CHECKPOINT:
                    return [Astrub.LEFT_CITY_CHECKPOINT[0] - 1, Astrub.LEFT_CITY_CHECKPOINT[1]]
                return Astrub.LEFT_CITY_CHECKPOINT

            elif Astrub.is_below_city(to_location):
                if from_location == Astrub.BOTTOM_CITY_CHECKPOINT:
                    return [Astrub.BOTTOM_CITY_CHECKPOINT[0], Astrub.BOTTOM_CITY_CHECKPOINT[1] + 1]
                return Astrub.BOTTOM_CITY_CHECKPOINT

        # GOING IN the city
        elif Astrub.is_in_city(to_location):
            if Astrub.is_above_city(from_location):
                if from_location == [Astrub.TOP_CITY_CHECKPOINT[0], Astrub.TOP_CITY_CHECKPOINT[1] + 1]:
                    return Astrub.TOP_CITY_CHECKPOINT
                return [Astrub.TOP_CITY_CHECKPOINT[0], Astrub.TOP_CITY_CHECKPOINT[1] + 1]

            elif Astrub.is_left_city(from_location):
                if from_location == [Astrub.LEFT_CITY_CHECKPOINT[0] - 1, Astrub.LEFT_CITY_CHECKPOINT[1]]:
                    return Astrub.LEFT_CITY_CHECKPOINT
                return [Astrub.LEFT_CITY_CHECKPOINT[0] - 1, Astrub.LEFT_CITY_CHECKPOINT[1]]

            elif Astrub.is_below_city(from_location):
                if from_location == [Astrub.BOTTOM_CITY_CHECKPOINT[0], Astrub.BOTTOM_CITY_CHECKPOINT[1] + 1]:
                    return Astrub.BOTTOM_CITY_CHECKPOINT
                return [Astrub.BOTTOM_CITY_CHECKPOINT[0], Astrub.BOTTOM_CITY_CHECKPOINT[1] + 1]

        return to_location

    @staticmethod
    def get_bank_path(location) -> list:
        """ find path to the bank from anywhere
        :param location: location of the player
        :return: list of positions to go to in order to get to the bank
        """
        return Astrub.get_path(location, Astrub.BANK_LOCATION)

    @staticmethod
    def is_in_city(location):
        return Astrub.ASTRUB_BOTTOM_RIGHT[0] >= location[0] >= Astrub.ASTRUB_TOP_LEFT[0] \
               and Astrub.ASTRUB_BOTTOM_RIGHT[1] >= location[1] >= Astrub.ASTRUB_TOP_LEFT[1]

    @staticmethod
    def is_above_city(location):
        return location[1] < Astrub.ASTRUB_TOP_LEFT[1]

    @staticmethod
    def is_below_city(location):
        return location[1] > Astrub.ASTRUB_BOTTOM_RIGHT[1]

    @staticmethod
    def is_left_city(location):
        return location[0] < Astrub.ASTRUB_TOP_LEFT[0]

    @staticmethod
    def get_craft_building(job) -> CraftBuilding:
        """ get craft building for each jobs """
        if job == Jobs.PAYSAN:
            return CraftBuilding(
                location=[5, -21],
                door_position=(1063, 521),
                exit_position=(758, 725),
                machine_position=(1120, 394)
            )

        elif job == Jobs.BUCHERON:
            return CraftBuilding(
                location=[2, -16],
                door_position=(1066, 363),
                exit_position=(711, 608),
                machine_position=(1091, 484)
            )

        elif job == Jobs.ALCHIMIST:
            return CraftBuilding(
                location=[3, -21],
                door_position=(990, 580),
                exit_position=(714, 662),
                machine_position=(806, 347)
            )

        else:
            ErrorHandler.fatal_error(f"unhandled job {job}")