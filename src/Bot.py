from typing import List

import pyautogui as pg
import time
import os
import pytesseract
from PIL.Image import Image

from src.components.Inventory import Inventory
from src.components.craft.craft import Craft
from src.enum.positions import Positions
from src.enum.images import Images
from src.components.Fight import Fight
from src.components.Movement import Movement
from src.utils.ErrorHandler import ErrorHandler, ErrorType
from src.utils.utils_fct import read_map_location, check_is_ghost, wait_image, check_ok_button


class Bot:
    MAX_TIME_SCANNING = 60
    HARVEST_TIME = 2
    CONFIDENCE = 0.75

    def __init__(self, region_name: str, ressources: List[str], crafts: List[str] = None, city_name: str = None, max_allowed_ressources=0):
        self.images = {}
        self.clicked_pos = []

        self.ressources = ressources
        self.get_ressources_images(ressources)
        self.max_allowed_ressources = max_allowed_ressources

        self.Movement = Movement(region_name, ressources, city_name)
        self.Fight = Fight()
        self.Inventory = Inventory()
        self.Craft = Craft(craft_names=crafts, max_pods=Inventory.get_max_pods())

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

        elif check_ok_button(click=True):
            return

        elif check_is_ghost():
            self.Movement.go_to_phoenix()

        elif self.check_craft():
            self.craft_routine()

        elif self.check_pods():
            self.bank_routine()

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

            # check if has craft order
            if self.check_craft():
                self.craft_routine()
                continue

            # scan for ressources
            if self.Movement.location in self.Movement.path:
                found_one = self.scan()

                if ErrorHandler.is_error:
                    continue

                if found_one:
                    # check if fight has occurred
                    time.sleep(1)
                    if self.Fight.check_combat_started():
                        self.fight_routine()
                        continue

                    # check if character needs to go unload ressources to the bank
                    if self.check_pods():
                        self.bank_routine()
                        continue

            success = self.Movement.go_to_next_location()
            if not success:
                # check if was caught in a fight
                if self.Fight.check_combat_started():
                    self.fight_routine()
                    continue

    def scan(self) -> bool:
        """ scan the map for ressources """
        print('Scanning', end='')

        self.clicked_pos = []

        start = time.time()
        found_one = False
        is_any = True
        while is_any:
            print('.', end='')
            is_any = self.find_all_ressources()
            if not is_any or time.time() - start > self.MAX_TIME_SCANNING:
                break
            time.sleep(self.HARVEST_TIME)

        print("\n")
        return found_one

    def find_all_ressources(self):
        for ressource_name, images in self.images.items():
            # check if this ressource belong to this position
            if self.Movement.location not in self.Movement.region.RESSOURCES_LOCATIONS[ressource_name]:
                continue

            # check that this is not a "fake" location (only here to help path finding)
            if ressource_name == "fake":
                continue

            for image in images:
                isAny = self.find_ressource(image)
                if isAny:
                    return True

        return False

    def find_ressource(self, image: Image) -> bool:
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
    @staticmethod
    def check_pods():
        """ check number of pods by reading number of ressources in the quick inventory (faster than opening inventory
        but more subject to errors)"""
        if Inventory.last_time_check_pods is not None and time.time() - Inventory.last_time_check_pods < Inventory.CHECK_PODS_INTERVAL:
            return False

        return Inventory.check_pods()

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

    def check_craft(self) -> bool:
        """ check if a craft order has been sent to the bot """
        return self.Craft.is_crafting and self.Craft.craft_order is not None

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

    def bank_routine(self, unload_ressources: (str, List[str]) = None):
        """ go to the bank and unload ressources """
        print("Going to bank")

        # go to the bank
        self.Movement.go_to_bank()
        time.sleep(2)

        if ErrorHandler.is_error:
            return

        bank = self.Movement.city.bank

        # unload ressources in bank
        bank.open()
        time.sleep(1)

        # unload ressources in bank
        if unload_ressources is None:
            bank.unload_ressources()
        else:
            if isinstance(unload_ressources, str):
                unload_ressources = [unload_ressources]

            for ressource_name in unload_ressources:
                success = bank.transfer(ressource_name, from_bank=False)
                if not success:
                    ErrorHandler.warning(f"unable to transfer {ressource_name}")

        # transfer ressources for requested crafts if possible (success -> craft order is set)
        self.Craft.transfer_required_ressources()

        # close bank tab
        bank.close()

        # get out of the bank
        bank.exit()

    def craft_routine(self):
        if self.Craft.craft_order is None:
            ErrorHandler.error("Call for craft routine when craft_order is None")
            ErrorHandler.is_error = True

        if self.Craft.is_crafting is False:
            ErrorHandler.error("Call for craft routine when craft_order is None")
            ErrorHandler.is_error = True

        print(f"\nCraft ordered : {self.Craft.craft_order}")

        # init job/building
        job = self.Craft.get_job(self.Craft.craft_order)
        building = self.Movement.city.get_craft_building(job)

        # go to the craft building
        self.Movement.go_to(building.LOCATION)

        # enter the requested building for the craft
        building.enter()
        time.sleep(3)

        # craft the requested ordered
        building.use_machine()
        building.craft(self.Craft.craft_order)
        building.exit_machine()

        time.sleep(1)

        # exit building
        building.exit()

        # go to bank to unload
        unload_ressource = self.Craft.craft_order
        self.Craft.craft_order = None
        self.bank_routine(unload_ressources=unload_ressource)

    # ==================================================================================================================
    # FIGHT
    def on_death(self):
        self.Movement.location = read_map_location()

    # ==================================================================================================================
    # DEBUG
    def test(self):
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

    @staticmethod
    def take_screenshot():
        img = pg.screenshot()
        dir = 'images/fight/'
        n_images = len(os.listdir(dir))
        img.save(dir + f'houblon_{n_images}.png')
        time.sleep(1)




