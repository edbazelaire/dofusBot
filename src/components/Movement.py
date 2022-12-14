from src.enums import Locations, Positions, Ressources, Images

import pyautogui as pg
import pytesseract
import time

from src.utils.ErrorHandler import ErrorHandler


class Movement:
    TRAVEL_MAP_TIME = 10
    LOAD_MAP_TIME = 10

    MAPS_LIST = {
        Ressources.HOUBLON: [
            [6, -22],
            [5, -24],
            [5, -26],
            [4, -26],
            [4, -28],
            [3, -30],
            [5, -28],
            [7, -23],  # fake position, to help path finding
            [8, -23],
        ],

        Ressources.BLE: [
            [5, -22],
            [3, -22],
            [3, -23],
            [4, -23],
            [5, -25],
            [3, -26],
            [4, -27],
            [4, -29],
            [4, -30],
            [5, -30],
            [6, -30],
            [6, -29],
            [6, -28],
            [5, -28],
            [7, -25],
            [7, -23],
        ]
    }

    def __init__(self, ressources: list):
        self.maps = []
        self.clicked_pos = []

        self.get_maps(ressources)

        self.current_map_index = 0
        self.position = (0, 0)
        self.next_position = None

        self.reset()

    # ==================================================================================================================
    # INITIALIZATION
    def reset(self):
        self.current_map_index = 0
        self.position = self.read_map_pos()

        if self.position in self.maps:
            self.current_map_index = self.maps.index(self.position)

    def get_maps(self, ressources):
        """ get unique position of each ressources """
        for ressource_name in ressources:
            pos = self.MAPS_LIST[ressource_name]
            [self.maps.append(pos[i]) for i in range(len(pos)) if pos[i] not in self.maps]

    # ==================================================================================================================
    def get_next_position(self):
        if self.next_position is None:
            self.next_position = self.maps[self.current_map_index]

        elif self.next_position == self.position:
            self.current_map_index = (self.current_map_index + 1) % len(self.maps)
            self.next_position = self.maps[self.current_map_index]

    def go_to_next_pos(self):
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

        self.go_to(self.next_position)

    def go_to(self, pos):
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
                    return
                retry_ctr += 1
                time.sleep(2)

                if last_position != self.position:
                    ErrorHandler.error("position changed while movement did not succeed")

                continue

            time.sleep(1)
            self.check_position()
            print(f'     position : {self.position}')
            retry_ctr = 0
            print("")

            distance_x = pos[0] - self.position[0]
            distance_y = pos[1] - self.position[1]

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
        # read x, y
        img = pg.screenshot(region=Positions.MAP_LOCATION_REG)
        img = Images.change_color(img)
        value = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789,-')

        try:
            split = value.split(',')
            x = int(split[0])
            y = int(split[1])
        except:
            ErrorHandler.error(f"unable to read position ({value})")
            return None

        if not with_zone:
            return [x, y]

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
        self.go_to(self.maps[0])
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
            if ErrorHandler.MAP_POSITION_ERROR >= 3:
                ErrorHandler.is_error = True
            return

        ErrorHandler.MAP_POSITION_ERROR = 0
