from typing import List
import pyautogui as pg
import time
import os
import pytesseract
from PIL.Image import Image

from src.enum.positions import Positions
from src.enum.images import Images
from src.components.Fight import Fight
from src.components.Movement import Movement
from src.utils.ErrorHandler import ErrorHandler
from src.utils.utils_fct import wait_click_on, check_map_loaded, read_map_location, check_is_ghost, open_inventory, wait_image


class Bot:
    MAX_TIME_SCANNING = 60
    HARVEST_TIME = 2
    CONFIDENCE = 0.75

    def __init__(self, region_name: str, ressources: List[str], window = None, city_name: str = None, max_allowed_ressources=0):
        self.images = {}
        self.window = window

        self.ressources = ressources
        self.get_ressources_images(ressources)
        self.max_allowed_ressources = max_allowed_ressources

        self.clicked_pos = []

        self.Movement = Movement(region_name, ressources, city_name)
        self.Fight = Fight()

        if Positions.WINDOW_SIZE_PERC <= 0.5:
            Bot.CONFIDENCE = 0.7

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

        # elif self.check_pods():
        elif self.check_inventory_pods():
            self.bank_routine()

        else:
            self.Movement.go_to_next_location()

    def get_ressources_images(self, ressources: list):
        """ get only images of requested ressources """
        dir = 'images/ressources'
        for ressource_name in ressources:
            self.images[ressource_name] = [Images.load(dir + '/' + filename) for filename in os.listdir(dir) if filename.startswith(ressource_name)]

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
            if self.Movement.location in self.Movement.region.path:
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

            self.Movement.go_to_next_location()

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

    def check_ressource(self, image: Image) -> bool:
        all_pos = list(pg.locateAllOnScreen(
            image,
            confidence=self.CONFIDENCE,
            region=Positions.WINDOW_REG
        ))

        for pos in all_pos:
            if (pos[0], pos[1]) in self.clicked_pos:
                continue

            self.clicked_pos.append((pos[0], pos[1]))

            if Positions.X_MAX > pos[0] > Positions.X_MIN and Positions.Y_MAX > pos[1] > Positions.Y_MIN:
                x = min(pos[0] + pos.width / 2, Positions.X_MAX)
                y = min(pos[1] + pos.height / 2, Positions.Y_MAX)
                pg.click(x, y)
                return True

        return False

    # ==================================================================================================================
    # CHECKS
    def check_pods(self):
        """ check number of pods by reading number of ressources in the quick inventory (faster than opening inventory
        but more subject to errors)"""
        num_ressources = self.read_num_ressources()

        # security : check that calculated number of ressources is not impossible
        if num_ressources >= self.max_allowed_ressources:
            if self.check_inventory_pods():
                print(f"MAX PODS : {num_ressources}")
                return True
        return False

    @staticmethod
    def check_inventory_pods():
        test = False

        open_inventory()
        wait_image(Images.INVENTORY_LOADED_ICON)
        time.sleep(1)

        img = pg.screenshot(region=Positions.INVENTORY_PODS_REG)
        height, width = img.size
        image_data = img.load()
        min_value = 150

        for loop1 in range(height):
            for loop2 in range(width):
                r, g, b = image_data[loop1, loop2]
                if r >= min_value or g >= min_value or b >= min_value:
                    test = True
                    break

            if test:
                break
        # close inventory
        open_inventory()
        time.sleep(1)

        return test

    @staticmethod
    def read_num_ressources(debug=False):
        """ read number of ressources displayed on quick inventory """
        num_ressources = 0
        for region in Positions.get_ressource_regions():
            img = pg.screenshot(region=region)
            img = img.resize((200, 100))
            img = Images.change_color(img, min_value=100)
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
        """ routine of actions to take when a fight occurs """
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
        time.sleep(2)

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
        wait_click_on(self.Movement.city.BANK_NPC_IMAGE, confidence=0.6)

        # click on "accept" to access your bank inventory
        wait_click_on(Images.get(Images.BANK_DIALOG_ACCESS), confidence=0.6)
        time.sleep(1)

        # select ressources tab
        wait_click_on(Images.get(Images.BANK_RESSOURCE_TAB), region=Positions.BANK_PLAYER_INVENTORY_REG, confidence=0.6)
        time.sleep(1)

        # unload ressources
        wait_click_on(Images.get(Images.BANK_TRANSFER_BUTTON), region=Positions.BANK_PLAYER_INVENTORY_REG, confidence=0.7)
        time.sleep(1)

        # validate ressources unloading
        wait_click_on(Images.get(Images.BANK_TRANSFER_VISIBLE_OBJ_BTN), confidence=0.6)
        time.sleep(1)

        # close bank
        pg.click(*Positions.CLOSE_BANK_BUTTON_POSITION)

    # ==================================================================================================================
    # FIGHT
    @staticmethod
    def join_fight():
        wait_click_on(Images.JOIN_FIGHT_IMG)

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
        img = img.resize((150, 30))
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


