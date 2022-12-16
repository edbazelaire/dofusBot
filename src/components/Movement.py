import itertools
import json
import math
from typing import List

from src.enum.positions import Positions
from src.enum.images import Images
from src.enum.locations import Locations

import pyautogui as pg
import pytesseract
import time

from src.utils.ErrorHandler import ErrorHandler


class Movement:
    TRAVEL_MAP_TIME = 10
    LOAD_MAP_TIME = 10

    def __init__(self, region: str, ressources: list):
        self.region = region
        self.path = []
        self.clicked_pos = []

        self.get_maps(ressources)

        self.current_map_index = 0
        self.position = (0, 0)
        self.next_position = None

        self.reset()

    # ==================================================================================================================
    # INITIALIZATION
    def reset(self):
        self.position = self.read_map_pos()

        if self.position in self.path:
            self.current_map_index = self.path.index(self.position)

    def get_maps(self, ressources: list):
        """ get unique position of each ressources """
        for ressource_name in ressources:
            pos = Locations.RESSOURCES_LOCATIONS[self.region][ressource_name]
            [self.path.append(pos[i]) for i in range(len(pos)) if pos[i] not in self.path]

        path = self.get_json_path(ressources, self.region)
        if path is not None and len(path) == len(self.path):
            print(f'Loaded path : {self.path}')
            self.path = path
            return

        self.path = self.get_best_path(self.path, from_checkpoint=Locations.GATES_LOCATION)
        self.save_json_path(ressources, self.region, self.path)
        print(f'Path : {self.path}')

    @staticmethod
    def get_json_path(ressources: list, region: str):
        with open('data/paths.json') as json_file:
            data = json.load(json_file)
            ressources.sort()
            name = '_'.join(ressources)
            if data is None or region not in data.keys() or name not in data[region].keys():
                return None
            return data[region][name]

    @staticmethod
    def save_json_path(ressources: list, region: str,  path: list):
        with open('data/paths.json', 'r') as json_file:
            all_paths = json.load(json_file)

        with open('data/paths.json', 'w') as json_file:
            ressources.sort()
            name = '_'.join(ressources)
            if region not in all_paths.keys():
                all_paths[region] = {}
            all_paths[region][name] = path
            json.dump(all_paths, json_file)

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

        # if next pos or pos is in astrub while the other is above astrub -> go to GATES
        if Locations.is_above_astrub(self.position) and Locations.is_in_astrub(self.next_position) \
                or Locations.is_in_astrub(self.position) and Locations.is_above_astrub(self.next_position):
            self.go_to(Locations.GATES_LOCATION)

        # BELOW astrub -> ABOVE astrub
        elif Locations.is_below_astrub(self.position) and Locations.is_above_astrub(self.next_position):
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
            self.check_position()

            print(f'     position : {self.position}')
            retry_ctr = 0
            print("")

            # if during the movement, the bot stumble on a harvesting map, return false to scan the map
            if self.position in self.path:
                return False

            distance_x = pos[0] - self.position[0]
            distance_y = pos[1] - self.position[1]

        return True

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
        return self.check_map_change()

    @staticmethod
    def read_map_pos(with_zone=False):
        """ get map location from GUID reading """
        x, y = 0, 0
        success = False

        # check a small range of configurations to allow rechecking if OCR cant read the map properly
        for i in range(10):
            # read x, y
            img = pg.screenshot(region=Positions.MAP_LOCATION_REG)
            if i % 2 == 0:
                img = img.resize((200, 75))
            img = Images.change_color(img, min_value=210 + (i // 2) * 3)
            value = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789,-')

            try:
                split = value.split(',')
                x = int(split[0])
                y = int(split[1])

                if abs(x) > 100 or abs(y) > 100:
                    continue

                success = True

                if not with_zone:
                    return [x, y]

                break
            except:
                continue

        if not success:
            ErrorHandler.error(f"unable to read position ({value})")
            return None

        # read Zone
        img = pg.screenshot(region=Positions.MAP_ZONE_NAME_REG)
        zone_name = pytesseract.image_to_string(img)

        return [x, y, zone_name]

    def get_back_to_first_position(self):
        """ go back to first position by getting threw the gates (meaning that we can access this position from either
        in or outside the city) """

        # go to the gates
        self.go_to(Locations.GATES_LOCATION)

        # go to first map and reset all values
        self.go_to(self.path[0])
        self.reset()

    def go_to_bank(self):
        if Locations.is_above_astrub(self.position):
            print(f"{self.position} : Moving to the GATES")
            self.go_to(Locations.GATES_LOCATION)

        print(f"{self.position} : Moving to the BANK")
        self.go_to(Locations.BANK_LOCATION)

        # get in the bank
        print(f"{self.position} : Clicking on BANK_DOOR")
        test = self.enter_building(Positions.BANK_DOOR_POSITION, loading_img=Images.get_bank(Images.BANK_NPC))

        if not test:
            return

        time.sleep(1)

        print(f"{self.position} : I am in the bank")

    @staticmethod
    def enter_building(click_pos: tuple, loading_img: str = '') -> bool:
        """ Enter a building by clicking requested position
        :param click_pos:   position to click to enter the building
        :param loading_img: waiting for this image to confirm map loading
        :return:
        """
        start = time.time()
        pg.click(*click_pos)
        if loading_img != '':
            while pg.locateOnScreen(loading_img) is None:
                if time.time() - start > 5:
                    ErrorHandler.is_error = True
                    return False
                time.sleep(0.5)

        return True

    # ==================================================================================================================
    # CHECKS
    def check_map_change(self, do_map_load_check=True) -> bool:
        """ check if player changed map by looking at map position """
        map_pos = self.read_map_pos()
        start = time.time()
        while map_pos == self.read_map_pos():
            if time.time() - start > self.TRAVEL_MAP_TIME:
                print("WARNING !! MAP NOT CHANGED")
                return False
            time.sleep(0.5)

        print("     MAP CHANGED")

        if do_map_load_check:
            self.check_map_loaded()
        return True

    def check_map_loaded(self) -> bool:
        """ check if player changed map by looking at map position """
        start = time.time()
        while True:
            if time.time() - start > self.LOAD_MAP_TIME:
                print(" -- map NOT loaded !!")
                return False

            confidence = 0.7
            pg.moveTo(*Positions.CHANGE_MAP_LEFT_POS)
            if pg.locateOnScreen('images/screenshots/cursor_left.png', confidence=confidence) is not None:
                print("     -- map loaded ")
                return True

            pg.moveTo(*Positions.CHANGE_MAP_RIGHT_POS)
            if pg.locateOnScreen('images/screenshots/cursor_right.png', confidence=confidence) is not None:
                print("     -- map loaded")
                return True

            pg.moveTo(*Positions.CHANGE_MAP_UP_POS)
            if pg.locateOnScreen('images/screenshots/cursor_up.png', confidence=confidence) is not None:
                print("     -- map loaded")
                return True

            pg.moveTo(*Positions.CHANGE_MAP_DOWN_POS)
            if pg.locateOnScreen('images/screenshots/cursor_down.png', confidence=confidence) is not None:
                print("     -- map loaded")
                return True

            time.sleep(0.1)

    def check_position(self):
        pos = self.read_map_pos()
        if self.position[0] != pos[0] or self.position[1] != pos[1]:
            ErrorHandler.error(f"position calculated {self.position} is different from OCR position {pos}")
            ErrorHandler.MAP_POSITION_ERROR += 1
            if ErrorHandler.MAP_POSITION_ERROR >= 2:
                ErrorHandler.is_error = True
            return

        ErrorHandler.MAP_POSITION_ERROR = 0

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
