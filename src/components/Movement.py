from typing import List

from src.enum.actions import Actions
from src.enum.images import Images
from src.enum.positions import Positions
from src.enum.locations import Locations

import pyautogui as pg
import time

from src.enum.regions import Regions
from src.location_handling.city.abstract_city import AbstractCity
from src.location_handling.regions.abstract_region import AbstractRegion
from src.location_handling.utils import get_region, get_city
from src.utils.ErrorHandler import ErrorHandler
from src.utils.utils_fct import read_map_location, wait_click_on, check_map_change, get_distance


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

        self.current_path_index = 0     # index in the farming path (
        self.location = (0, 0)          # current position of the bot
        self.next_location = None       # location that the bot is currently heading to

        self.location = read_map_location()

        if self.location in self.path:
            self.current_path_index = self.path.index(self.location)

    # ==================================================================================================================
    # INITIALIZATION
    def reset(self):
        self.location = read_map_location()

    # ==================================================================================================================
    def get_next_position(self):
        if self.next_location is None:
            self.next_location = self.path[self.current_path_index]

        elif self.next_location == self.location:
            self.current_path_index = (self.current_path_index + 1) % len(self.path)
            self.next_location = self.path[self.current_path_index]

    def go_to_next_pos(self):
        """ return True if reaches next pos, False if stop during movement """
        # security, if a None pos is provided
        if self.next_location is None:
            self.get_next_position()

        # get to next map
        if self.location == self.next_location:
            self.get_next_position()

        # ANYWHERE -> IN CITY or IN CITY -> ANYWHERE
        if self.city.is_in_city(self.next_location) or self.city.is_in_city(self.location):
            path = self.city.get_path(from_location=self.location, to_location=self.next_location)
            self.follow_path(path)

        # TODO : put in Region
        elif get_distance(self.location, self.next_location) > 15:
            self.location = read_map_location()
            success = False
            for i in range(3):
                Actions.do(Actions.TAKE_RECALL_POTION)
                if self.location != read_map_location():
                    self.location = read_map_location()
                    success = True
                    break

            if not success:
                ErrorHandler.fatal_error("unable to take recall potion")

        return self.go_to(self.next_location)

    def go_to(self, pos) -> bool:
        """ go to a position, if bot is stopping for any reason, return false. Return True if reaches max position """

        print('=' * 100)
        print(f'Going to : {pos}')

        self.clicked_pos = []
        distance_x = pos[0] - self.location[0]
        distance_y = pos[1] - self.location[1]

        retry_ctr = 0
        max_retry = 3

        while distance_y != 0 or distance_x != 0:
            success = False
            last_position = self.location
            if distance_x > 0:
                success = self.move_right()

            elif distance_x < 0:
                success = self.move_left()

            elif distance_y > 0:
                success = self.move_down()

            elif distance_y < 0:
                success = self.move_up()

            if not success:
                if retry_ctr == max_retry:
                    print("ERROR : MAX RETRY MOVEMENT")
                    ErrorHandler.is_error = True
                    return False
                retry_ctr += 1
                time.sleep(2)

                if last_position != self.location:
                    ErrorHandler.error("position changed while movement did not succeed")

                continue

            # sleep (safety) and check position with OCR position
            time.sleep(1)
            self.location = read_map_location()

            print(f'     location : {self.location}')
            retry_ctr = 0
            print("")

            # if during the movement, the bot stumble on a harvesting map, return false to scan the map
            if self.location in self.path:
                return False

            distance_x = pos[0] - self.location[0]
            distance_y = pos[1] - self.location[1]

        return True

    def follow_path(self, path: list):
        for value in path:
            if Actions.is_action(value):
                Actions.do(value)
                self.location = read_map_location()
            else:
                self.go_to(value)

    def move_left(self):
        if not self.move(Positions.CHANGE_MAP_LEFT_POS):
            return False
        return True

    def move_right(self):
        if not self.move(Positions.CHANGE_MAP_RIGHT_POS):
            return False
        return True

    def move_up(self):
        if not self.move(Positions.CHANGE_MAP_UP_POS):
            return False
        return True

    def move_down(self):
        if not self.move(Positions.CHANGE_MAP_DOWN_POS):
            return False
        return True

    @staticmethod
    def move(click_pos):
        pg.click(*click_pos)
        return check_map_change(from_location=read_map_location())

    def get_back_to_first_position(self):
        """ go back to first position by getting threw the gates (meaning that we can access this position from either
        in or outside the city) """

        if self.region == Regions.CHAMP_ASTRUB:
            # go to the gates
            self.go_to(Locations.GATES_LOCATION)
        else:
            Actions.do(Actions.TAKE_RECALL_POTION)
            self.location = read_map_location()

        # go to first map and reset all values
        self.go_to(self.path[0])
        self.reset()

    def go_to_bank(self):
        print(f"{self.location} : Moving to the BANK")
        success = False
        while not success:
            path = self.city.get_bank_path(self.location)
            self.follow_path(path)

            # SAFETY
            ocr_location = read_map_location()
            if ocr_location != self.city.BANK_LOCATION:
                ErrorHandler.error(f"ocr location ({ocr_location}) is not on bank location ({self.city.BANK_LOCATION})")
                self.location = ocr_location
                continue

            success = True

        # get in the bank
        print(f"{self.location} : Clicking on BANK_DOOR")
        test = self.enter_building(click_pos=self.city.BANK_DOOR_POSITION, loading_img=self.city.BANK_NPC_IMAGE)

        if not test:
            return

        time.sleep(1)

        print(f"{self.location} : I am in the bank")

    @staticmethod
    def enter_building(click_pos: tuple = None, click_img: str = None, loading_img: str = '') -> bool:
        """ Enter a building by clicking requested position
        :param click_pos:   position to click to enter the building
        :param click_img:   image to click in order to get in the building
        :param loading_img: waiting for this image to confirm map loading
        :return:
        """

        if click_pos is not None:
            pg.click(*click_pos)

        elif click_img is not None:
            wait_click_on(click_img)

        else:
            ErrorHandler.fatal_error("BAD CONFIGURATION, neither click_pos or click_img is provided")

        start = time.time()
        if loading_img != '':
            while pg.locateOnScreen(loading_img) is None:
                if time.time() - start > 5:
                    ErrorHandler.is_error = True
                    return False
                time.sleep(0.5)

        return True

    # ==================================================================================================================
    # ROUTINES
    def ghost_routine(self):
        """ get back to phoenix statue and then to the farming locations """
        print("-- is ghost")
        wait_click_on('images/screenshots/yes_button.png')

        # wait that map is loaded
        check_map_change(from_location=self.location)

        wait_click_on(Images.get_fight(Images.CANCEL_POPUP), offset_x=5, offset_y=5)

        self.go_to_phoenix()

    def go_to_phoenix(self):
        self.location = read_map_location()
        self.follow_path(self.region.get_phoenix_path())

        wait_click_on(self.region.PHOENIX_STATUE_IMAGE, offset_x=10)

        # wait until reaching phoenix statue
        time.sleep(3)

    # ==================================================================================================================
    # CHECKS
    def check_location(self):
        pos = read_map_location()
        if self.location[0] != pos[0] or self.location[1] != pos[1]:
            ErrorHandler.error(f"position calculated {self.location} is different from OCR position {pos}")
            ErrorHandler.MAP_POSITION_ERROR += 1
            if ErrorHandler.MAP_POSITION_ERROR >= ErrorHandler.MAP_POSITION_ERROR_MAX:
                ErrorHandler.is_error = True
            return False

        ErrorHandler.MAP_POSITION_ERROR = 0
        return True

