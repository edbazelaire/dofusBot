import itertools
import json
import math
from typing import List

from src.entity.city.abstract_city import AbstractCity
from src.entity.city.astrub import Astrub
from src.entity.city.bonta import Bonta
from src.enum.actions import Actions
from src.enum.positions import Positions
from src.enum.images import Images
from src.enum.locations import Locations

import pyautogui as pg
import time

from src.enum.regions import Regions
from src.utils.ErrorHandler import ErrorHandler
from src.utils.JsonHandler import JsonHandler
from src.utils.utils_fct import read_map_location, wait_click_on, check_map_change


class Movement:
    def __init__(self, region: str, ressources: list, city: AbstractCity = None):
        self.region = region
        self.city = self.get_closest_city(region) if city is None else city
        self.path = []
        self.clicked_pos = []

        self.set_path(ressources)

        self.current_map_index = 0
        self.position = (0, 0)
        self.next_position = None

        self.position = read_map_location()

        if self.position in self.path:
            self.current_map_index = self.path.index(self.position)

    # ==================================================================================================================
    # INITIALIZATION
    def reset(self):
        self.position = read_map_location()

    def set_path(self, ressources: list):
        """ get unique position of each ressources """
        for ressource_name in ressources:
            pos = Locations.RESSOURCES_LOCATIONS[self.region][ressource_name]
            [self.path.append(pos[i]) for i in range(len(pos)) if pos[i] not in self.path]

        path = JsonHandler.get_json_path(ressources, self.region)
        if path is not None and len(path) == len(self.path):
            print(f'Loaded path : {self.path}')
            self.path = path
            return

        self.path = self.get_best_path(self.path, from_checkpoint=Locations.GATES_LOCATION)
        JsonHandler.save_json_path(ressources, self.region, self.path)
        print(f'Path : {self.path}')

    @staticmethod
    def get_closest_city(region) -> AbstractCity:
        if region == Regions.CHAMP_ASTRUB:
            return Astrub()
        else:
            return Bonta()

    # ==================================================================================================================
    def get_next_position(self):
        if self.next_position is None:
            self.next_position = self.path[self.current_map_index]

        elif self.next_position == self.position:
            self.current_map_index = (self.current_map_index + 1) % len(self.path)
            self.next_position = self.path[self.current_map_index]

    def go_to_next_pos(self):
        """ return True if reaches next pos, False if stop during movement """
        # security, if a None pos is provided
        if self.next_position is None:
            self.get_next_position()

        # ANYWHERE -> IN CITY or IN CITY -> ANYWHERE
        if self.city.is_in_city(self.next_position) or self.city.is_in_city(self.position):
            path = self.city.get_path(from_location=self.position, to_location=self.next_position)
            self.follow_path(path)

        # TODO : change that in region maybe
        # BELOW astrub -> ABOVE astrub
        elif Astrub.is_below_city(self.position) and Astrub.is_above_city(self.next_position):
            self.go_to(Locations.TOP_CORNER_CITY_LOCATION)

        return self.go_to(self.next_position)

    def go_to(self, pos) -> bool:
        """ go to a position, if bot is stopping for any reason, return false. Return True if reaches max position """

        print('=' * 100)
        print(f'Going to : {pos}')

        self.clicked_pos = []
        distance_x = pos[0] - self.position[0]
        distance_y = pos[1] - self.position[1]

        retry_ctr = 0
        max_retry = 3

        while distance_y != 0 or distance_x != 0:
            success = False
            last_position = self.position
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

                if last_position != self.position:
                    ErrorHandler.error("position changed while movement did not succeed")

                continue

            # sleep (safety) and check position with OCR position
            time.sleep(1)
            self.check_location()

            print(f'     position : {self.position}')
            retry_ctr = 0
            print("")

            # if during the movement, the bot stumble on a harvesting map, return false to scan the map
            if self.position in self.path:
                return False

            distance_x = pos[0] - self.position[0]
            distance_y = pos[1] - self.position[1]

        return True

    def follow_path(self, path: list):
        for value in path:
            if Actions.is_action(value):
                Actions.do(value)
            else:
                self.go_to(value)

    def move_left(self):
        if not self.move(Positions.CHANGE_MAP_LEFT_POS):
            return False

        self.position[0] -= 1
        return True

    def move_right(self):
        if not self.move(Positions.CHANGE_MAP_RIGHT_POS):
            return False

        self.position[0] += 1
        return True

    def move_up(self):
        if not self.move(Positions.CHANGE_MAP_UP_POS):
            return False

        self.position[1] -= 1
        return True

    def move_down(self):
        if not self.move(Positions.CHANGE_MAP_DOWN_POS):
            return False

        self.position[1] += 1
        return True

    def move(self, click_pos):
        pg.click(*click_pos)
        return check_map_change(from_location=read_map_location())

    def get_back_to_first_position(self):
        """ go back to first position by getting threw the gates (meaning that we can access this position from either
        in or outside the city) """

        # go to the gates
        self.go_to(Locations.GATES_LOCATION)

        # go to first map and reset all values
        self.go_to(self.path[0])
        self.reset()

    def go_to_bank(self):
        print(f"{self.position} : Moving to the BANK")
        success = False
        while not success:
            path = self.city.get_bank_path(self.position)
            self.follow_path(path)

            # SAFETY
            ocr_location = read_map_location()
            if ocr_location != self.city.BANK_LOCATION:
                ErrorHandler.error(f"ocr location ({ocr_location}) is not on bank location ({self.city.BANK_LOCATION})")
                self.position = ocr_location
                continue

            success = True

        # get in the bank
        print(f"{self.position} : Clicking on BANK_DOOR")
        test = self.enter_building(click_pos=self.city.BANK_CLICK_POSITION, loading_img=self.city.BANK_NPC_IMAGE)

        if not test:
            return

        time.sleep(1)

        print(f"{self.position} : I am in the bank")

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
            success = wait_click_on(click_img)

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
    # CHECKS
    def check_location(self):
        pos = read_map_location()
        if self.position[0] != pos[0] or self.position[1] != pos[1]:
            ErrorHandler.error(f"position calculated {self.position} is different from OCR position {pos}")
            ErrorHandler.MAP_POSITION_ERROR += 1
            if ErrorHandler.MAP_POSITION_ERROR >= ErrorHandler.MAP_POSITION_ERROR_MAX:
                ErrorHandler.is_error = True
            return False

        ErrorHandler.MAP_POSITION_ERROR = 0
        return True

    # ==================================================================================================================
    # UTILS
    @staticmethod
    def get_distance(pos1: list, pos2: list):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def get_best_path(all_pos: List[List[int]], from_checkpoint: List[int]) -> List[List[int]]:
        """
        calculate most optimized path for all given positions
        :param all_pos:         list of all positions that the bot is supposed to go to
        :param from_checkpoint: checkpoint from where the char arrives
        :return:
        """

        # get index of the position closest to the checkpoint
        start_pos_index = None
        for i in range(len(all_pos)):
            if start_pos_index is None or Movement.get_distance(all_pos[start_pos_index], from_checkpoint) > Movement.get_distance(all_pos[i], from_checkpoint):
                start_pos_index = i

        # pop closest position from all positions as start position
        start_pos = all_pos.pop(0)

        # from remaining positions, calculate the shortest path
        best_distance = math.inf
        best_path = []
        for path in itertools.permutations(all_pos, len(all_pos)):
            distance = 0
            last_pos = start_pos
            for pos in path:
                relative_distance = Movement.get_distance(pos, last_pos)
                if relative_distance > 6:
                    distance = math.inf
                    break

                distance += relative_distance

                if distance >= best_distance:
                    distance = math.inf
                    break

                last_pos = pos

            # -- get back to start position
            distance += Movement.get_distance(start_pos, last_pos)

            # -- check if distance is shorter
            if distance < best_distance:
                best_path = list(path)
                best_distance = distance

        return [start_pos] + best_path
