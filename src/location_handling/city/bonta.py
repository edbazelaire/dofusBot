from src.buildings.Bank import Bank
from src.buildings.craft_building import CraftBuilding
from src.enum.jobs import Jobs
from src.location_handling.city.abstract_city import AbstractCity
from src.enum.actions import Actions
from src.enum.images import Images
from src.utils.ErrorHandler import ErrorHandler


class Bonta(AbstractCity):
    NAME = 'Bonta'
    SUB_REGION = ''

    CITY_TOP_CORNER = [-37, -61]
    CITY_BOTTOM_CORNER = [-26, -50]

    BANK_LOCATION = [-31, -57]

    def __init__(self):
        super().__init__()

        self.bank = Bank(
            location=self.BANK_LOCATION,
            door_position=(964, 677),
            exit_position=(519, 798),
            npc_image=Images.BANK_NPC_BONTA
        )

    @staticmethod
    def is_in_city(location):
        return Bonta.CITY_BOTTOM_CORNER[0] >= location[0] >= Bonta.CITY_TOP_CORNER[0] \
            and Bonta.CITY_BOTTOM_CORNER[1] >= location[1] >= Bonta.CITY_TOP_CORNER[1]

    @staticmethod
    def get_aiming_location(from_location, to_location):
        """ next location to go to in order to be able to go to requested location """
        # -------------------------------------------------------------------
        # IN / OUT of the city
        if Bonta.is_in_city(from_location) and not Bonta.is_in_city(to_location):
            return Actions.TAKE_RECALL_POTION

        elif Bonta.is_in_city(to_location) and not Bonta.is_in_city(from_location):
            return Actions.TAKE_BONTA_POTION

        # -------------------------------------------------------------------
        # STAIRS (start 1)
        # stairs 1
        elif from_location == [-31, -52] and to_location[1] <= -53:
            return [Actions.CLICK_ON, (1108, 66)]

        # go to the closest stairs
        elif Bonta.is_in_city(from_location) \
                and from_location[1] >= -52 and to_location[1] <= -53 \
                and from_location != [-31, -52]:
            return [-31, -52]

        # -------------------------------------------------------------------
        # STAIRS (start 2)
        # stairs 1
        elif from_location == [-32, -55] and to_location[1] <= -56:
            return [Actions.CLICK_ON, (1241, 258)]

        # stairs 2
        elif from_location == [-31, -55] and to_location[1] <= -56:
            return [Actions.CLICK_ON, (908, 257)]

        # go to the closest stairs
        elif Bonta.is_in_city(from_location) \
                and -53 >= from_location[1] >= -55 and to_location[1] <= -56 \
                and from_location != [-32, -55] and from_location != [-31, -55]:
            if to_location[0] <= -32:
                return [-32, -55]
            else:
                return [-31, -55]

        return to_location

    @staticmethod
    def get_craft_building(job) -> CraftBuilding:
        """ get craft building for each jobs """
        if job == Jobs.PAYSAN:
            return CraftBuilding(
                location=[-31, -52],
                door_position=(846, 565),
                exit_position=(1353, 537),
                machine_position=(768, 268),
                machine_img=Images.BONTA_BOULANGERIE
            )

        else:
            ErrorHandler.fatal_error(f"unhandled job {job}")