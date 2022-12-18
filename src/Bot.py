from typing import List

import pyautogui as pg
import time
import os
import pytesseract

from src.enum.positions import Positions
from src.enum.images import Images
from src.components.Fight import Fight
from src.components.Movement import Movement
from src.utils.ErrorHandler import ErrorHandler
from src.utils.utils_fct import wait_click_on, check_map_loaded, read_map_location, check_is_ghost


class Bot:
    MAX_TIME_SCANNING = 60
    HARVEST_TIME = 1
    CONFIDENCE = 0.7
    MAX_ALLOWED_RESSOURCES = 3000

    def __init__(self, region_name: str, ressources: List[str], city_name: str = None):
        self.images = {}

        self.ressources = ressources
        self.get_ressources_images(ressources)
        self.last_num_ressources_checked = 0

        self.clicked_pos = []

        self.Movement = Movement(region_name, ressources, city_name)
        self.Fight = Fight()

    # ==================================================================================================================
    # INITIALIZATION
    def reset(self):
        print("")
        print("=" * 50)
        print('|  RESET')
        print("=" * 50)
        print("")

        self.clicked_pos = []
        self.Movement.reset()
        ErrorHandler.reset()

        self.check_situation()

    def check_situation(self):
        """ on reset check the situation the character is in """
        if self.Fight.check_combat_started():
            self.fight_routine()

        elif self.check_tomb():
            self.Movement.ghost_routine()

        elif check_is_ghost():
            self.Movement.go_to_phoenix()

        elif self.check_pods():
            self.bank_routine()

        else:
            self.Movement.go_to_next_pos()

    def get_ressources_images(self, ressources: list):
        """ get only images of requested ressources """
        dir = 'images'
        for ressource_name in ressources:
            self.images[ressource_name] = [dir + '/' + filename for filename in os.listdir(dir) if filename.startswith(ressource_name)]

    # ==================================================================================================================
    # RUN
    def run(self):
        print(f"STARTING POSITION : {self.Movement.location}")
        print(f"STARTING MAP INDEX : {self.Movement.current_path_index}")

        self.check_situation()

        while True:
            if ErrorHandler.is_error:
                self.reset()

            # scan for ressources
            self.scan()

            if ErrorHandler.is_error:
                continue

            # check if fight has occurred
            time.sleep(1)
            if self.Fight.check_combat_started():
                self.fight_routine()
                continue

            if ErrorHandler.is_error:
                continue

            # check if character needs to go unload ressources to the bank
            if self.check_pods():
                self.bank_routine()
                continue

            if ErrorHandler.is_error:
                continue

            self.Movement.go_to_next_pos()

    def scan(self):
        """ scan the map for ressources """
        print('Scanning', end='')

        start = time.time()
        isAny = True
        while isAny:
            print('.', end='')
            isAny = self.check_all_ressources()
            if not isAny or time.time() - start > self.MAX_TIME_SCANNING:
                break
            found_one = True
            time.sleep(self.HARVEST_TIME)

        print("\n")

    def check_all_ressources(self):
        for ressource_name, images in self.images.items():
            # check if this ressource belong to this position
            if self.Movement.location not in self.Movement.region.RESSOURCES_LOCATIONS[ressource_name]:
                continue

            # check that this is not a "fake" location (only here to help path finding)
            if ressource_name == "fake":
                continue

            for image in images:
                isAny = self.check_ressource(image)
                if isAny:
                    return True

        return False

    def check_ressource(self, image) -> bool:
        all_pos = list(pg.locateAllOnScreen(
            image,
            confidence=self.CONFIDENCE,
            region=Positions.WINDOW_REG
        ))

        for pos in all_pos:
            if (pos[0], pos[1]) in self.clicked_pos:
                continue

            if Positions.X_MAX > pos[0] > Positions.X_MIN and Positions.Y_MAX > pos[1] > Positions.Y_MIN:
                pg.moveTo(pos[0], pos[1])
                time.sleep(0.5)
                pg.click(pos[0], pos[1])
                self.clicked_pos.append((pos[0], pos[1]))
                pg.moveTo(10, 10)   # move mouse to prevent overs
                return True

        return False

    # ==================================================================================================================
    # CHECKS
    def check_pods(self):
        """ check number of pods by reading number of ressources in the quick inventory (faster than opening inventory
        but more subject to errors)"""
        num_ressources = self.read_num_ressources()

        # security : check that calculated number of ressources is not impossible
        if self.last_num_ressources_checked != 0 \
                and num_ressources != 0 \
                and abs(num_ressources - self.last_num_ressources_checked) > 500:
            ErrorHandler.warning("OCR ressource bad ressource recognition : "
                                 + f"\n    - num ressources checked {num_ressources}"
                                 + f"\n    - last num ressources checked {self.last_num_ressources_checked}"
                                 )
            # return False

        self.last_num_ressources_checked = num_ressources
        if num_ressources >= self.MAX_ALLOWED_RESSOURCES:
            print(f"MAX PODS : {num_ressources}")
            return True
        return False

    @staticmethod
    def read_num_ressources(debug=False):
        """ read number of ressources displayed on quick inventory """
        num_ressources = 0
        for region in Positions.RESSOURCES_REG:
            img = pg.screenshot(region=region)
            img = img.resize((200, 100))
            img = Images.change_color(img, min_value=140)
            value = pytesseract.image_to_string(img, config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')

            if debug:
                print(value)
                img.show()

            value = 0 if value == '' else int(value)
            num_ressources += value

        if debug:
            print(f"num_ressources : {num_ressources}")
        return num_ressources

    @staticmethod
    def check_tomb() -> bool:
        """ check if TOMB image is on screen"""
        start = time.time()
        while True:
            if time.time() - start > 5:
                return False
            if pg.locateOnScreen('images/screenshots/tomb.png', confidence=0.7):
                return True

    # ==================================================================================================================
    # ROUTINES
    def fight_routine(self):
        """ routine of actions to take when a fight occures """
        self.Fight.fight()
        if self.Fight.check_is_victory():
            return

        if self.check_tomb():
            self.Movement.ghost_routine()
        elif self.Fight.check_is_defeat():
            self.on_death()

    def bank_routine(self):
        """ go to the bank and unload ressources """
        print("MAX PODS REACHED -> Going to bank")

        # go to the bank
        self.Movement.go_to_bank()

        if ErrorHandler.is_error:
            return

        # unload ressources in the bank
        self.unload_bank()
        time.sleep(1)

        # get out of the bank
        pg.click(*self.Movement.city.GET_OUT_BANK_POSITION)
        time.sleep(1)
        success = check_map_loaded()
        if not success:
            ErrorHandler.error("unable to get out of bank")

        # reset
        self.reset()

    def unload_bank(self):
        """ unload ressources in the bank """
        # click on npc
        wait_click_on(self.Movement.city.BANK_NPC_IMAGE, offset_x=15, offset_y=15)

        # click on "accept" to access your bank inventory
        wait_click_on(Images.get_bank(Images.BANK_DIALOG_ACCESS), offset_x=50, offset_y=10)
        time.sleep(1)

        # select ressources tab
        wait_click_on(Images.get_bank(Images.BANK_RESSOURCE_TAB), region=Positions.BANK_PLAYER_INVENTORY_REG, offset_x=5, offset_y=5, confidence=0.99)
        time.sleep(1)

        # unload ressources
        wait_click_on(Images.get_bank(Images.BANK_TRANSFER_BUTTON), offset_x=5, offset_y=5, confidence=0.99)
        time.sleep(1)

        # validate ressources unloading
        wait_click_on(Images.get_bank(Images.BANK_TRANSFER_VISIBLE_OBJ_BTN))
        time.sleep(1)

        # close bank
        pg.click(*Positions.CLOSE_BANK_BUTTON_POSITION)

    # ==================================================================================================================
    # FIGHT
    def on_death(self):
        self.Movement.location = read_map_location()

    # ==================================================================================================================
    # DEBUG
    def test(self):
        # self.test_ocr()
        self.Fight.fight()
        return

    @staticmethod
    def test_ocr_map():
        img = pg.screenshot(region=Positions.MAP_LOCATION_REG)
        value = pytesseract.image_to_string(img, config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789,-')

        print(value)
        img.show()

    @staticmethod
    def test_ocr_ressources():
        img = pg.screenshot(region=Positions.RESSOURCE4_REG)
        img = img.resize((200, 100))
        img = Images.change_color(img, min_value=140)
        value = pytesseract.image_to_string(img, config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')

        print(value)
        img.show()

    def take_screeshot(self):
        img = pg.screenshot()
        dir = 'images/fight/'
        n_images = len(os.listdir(dir))
        img.save(dir + f'houblon_{n_images}.png')
        time.sleep(1)


