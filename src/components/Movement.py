from typing import List

from src.enum.actions import Actions
from src.enum.images import Images
from src.enum.positions import Positions
from src.enum.locations import Locations

import pyautogui as pg
import time

from src.enum.regions import Regions
from src.location_handling.utils import get_region, get_city
from src.utils.ErrorHandler import ErrorHandler
from src.utils.utils_fct import read_map_location, wait_click_on, check_map_change, wait_image


class Movement:
    """
    Handle Bot's movements from a location to another
    """

    def __init__(self, region_name: str, ressources: List[str], city_name: str = None):
        """
        :param region_name: name of the region where the ressources are farmed
        :param ressources:  list of the ressources to farm in the Region
        :param city_name:   name of the city where the ressources are unloaded to the bank. If not provided, use default
                            city of the region
        """
        self.region = get_region(region_name, ressources)
        if city_name is None:
            city_name = self.region.CITY
        self.city = get_city(city_name)
        self.path = self.region.path

        self.clicked_pos = []

        self.current_path_index = 0     # index in the farming path
        self.current_path_index_modificator = 1
        self.location = (0, 0)          # current position of the bot
        self.next_location = None       # location that the bot is currently heading to

        self.location = read_map_location()

        if self.location in self.path:
            self.current_path_index = self.path.index(self.location)

    # ==================================================================================================================
    # INITIALIZATION
    def reset(self, with_current_index=False):
        self.location = read_map_location()
        if with_current_index:
            self.current_path_index = 0

    # ==================================================================================================================
    def get_next_location(self):
        if self.next_location is None:
            self.next_location = self.path[self.current_path_index]

        elif self.next_location == self.location:
            if self.current_path_index % (len(self.path) - 1) == 0:
                if self.region.IS_REVERSE_PATH:
                    self.current_path_index_modificator *= -1
                else:
                    self.current_path_index = 0

            self.current_path_index += self.current_path_index_modificator
            self.next_location = self.path[self.current_path_index]

    def go_to_next_location(self):
        """ return True if reaches next pos, False if stop during movement """
        # security, if a None pos is provided
        self.location = read_map_location()

        if self.next_location is None or self.location == self.next_location:
            self.get_next_location()

        # ANYWHERE -> IN CITY or IN CITY -> ANYWHERE
        if self.city.is_in_city(self.next_location) or self.city.is_in_city(self.location):
            path = self.city.get_path(from_location=self.location, to_location=self.next_location)
            self.follow_path(path)
            return

        path = self.region.get_path(self.location, self.next_location)
        self.follow_path(path)

    def go_to(self, pos, force=False) -> bool:
        """ go to a position, if bot is stopping for any reason, return false. Return True if reaches max position """

        print('=' * 100)
        print(f'Going to : {pos}')

        if pos == [-76, -47]:
            print('')

        self.clicked_pos = []
        distance_x = pos[0] - self.location[0]
        distance_y = pos[1] - self.location[1]

        while distance_y != 0 or distance_x != 0:
            # check movement priority between x and y
            starts_with_x = distance_y == 0 or self.current_path_index_modificator != -1

            if distance_x > 0 and starts_with_x:
                success = self.move_right()

            elif distance_x < 0  and starts_with_x:
                success = self.move_left()

            elif distance_y > 0:
                success = self.move_down()

            elif distance_y < 0:
                success = self.move_up()

            else:
                success = True

            if ErrorHandler.is_error:
                return False

            self.location = read_map_location()
            distance_x = pos[0] - self.location[0]
            distance_y = pos[1] - self.location[1]

            if success:
                # sleep (safety) and check position with OCR position
                time.sleep(1)

                print(f'     location : {self.location}')
                print("")

            # if during the movement, the bot stumble on a harvesting map, return false to scan the map
            if self.location in self.path and not force:
                return False

        return True

    def follow_path(self, path: list):
        for value in path:
            if Actions.is_action(value):
                Actions.do(value)
                self.location = read_map_location()
            else:
                self.go_to(value, force=True)

    def move_left(self):
        return self.move(Positions.CHANGE_MAP_LEFT_POS())

    def move_right(self):
        return self.move(Positions.CHANGE_MAP_RIGHT_POS())

    def move_up(self):
        return self.move(Positions.CHANGE_MAP_UP_POS())

    def move_down(self):
        return self.move(Positions.CHANGE_MAP_DOWN_POS())

    def move(self, click_pos):
        pg.click(*click_pos)
        return check_map_change(from_location=self.location)

    # ==================================================================================================================
    # ROUTINES
    def ghost_routine(self):
        """ get back to phoenix statue and then to the farming locations """
        print("-- is ghost")
        wait_click_on(Images.YES_BUTTON)

        # wait that map is loaded
        check_map_change(from_location=self.location)

        wait_click_on(Images.CANCEL_POPUP)

        self.go_to_phoenix()

    # ==================================================================================================================
    # GO TO SPECIFIC POSITION
    def go_to_phoenix(self):
        self.location = read_map_location()
        self.follow_path(self.region.get_phoenix_path())

        wait_click_on(self.region.PHOENIX_STATUE_IMAGE)

        # wait until reaching phoenix statue
        time.sleep(3)

    def go_to_bank(self):
        print(f"{self.location} : Moving to the BANK")
        success = False
        while not success:
            path = self.city.get_bank_path(self.location)
            self.follow_path(path)

            # SAFETY
            ocr_location = read_map_location()
            if ocr_location != self.city.bank.LOCATION:
                ErrorHandler.error(f"ocr location ({ocr_location}) is not on bank location ({self.city.bank.LOCATION})")
                self.location = ocr_location
                continue

            success = True

        # get in the bank
        time.sleep(2)
        print(f"{self.location} : Clicking on BANK_DOOR")
        test = self.city.bank.enter()

        if not test:
            return

        time.sleep(1)

        print(f"{self.location} : I am in the bank")

    # ==================================================================================================================
    # CHECKS
    def check_location(self):
        pos = read_map_location()
        if self.location[0] != pos[0] or self.location[1] != pos[1]:
            ErrorHandler.error(f"position calculated {self.location} is different from OCR position {pos}",
                               ErrorHandler.MAP_POSITION_ERROR)
            return False

        # reset if location check went ok
        ErrorHandler.ERROR_CTRS[ErrorHandler.MAP_POSITION_ERROR] = 0
        return True
