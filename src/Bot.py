from typing import List
import pyautogui as pg
import time
import os
import pytesseract

from data.JobRoutines import JobRoutine
from src.components.Inventory import Inventory
from src.components.Scanner import Scanner
from src.components.craft.craft import Craft
from src.enum.positions import Positions
from src.enum.images import Images
from src.components.Fight import Fight
from src.components.Movement import Movement
from src.enum.routines import Routines
from src.utils.CurrentBot import CurrentBot
from src.utils.ErrorHandler import ErrorHandler
from src.utils.Sleeper import Sleeper
from src.utils.utils_fct import read_map_location, check_is_ghost, check_ok_button, wait_click_on, check_map_change


class Bot:
    CURRENT_ID = 0
    MAX_TIME_SCANNING = 60

    def __init__(self, bot_id, window, job_routine: JobRoutine):
        self.current_routine: (None, Routines) = None
        self.current_step: int = 0

        self.id = bot_id
        self.window = window
        self.clicked_pos = []
        self.unload_ressources = []
        self.max_pods = 0 if len(job_routine.crafts) == 0 else Inventory.get_max_pods()

        self.Movement = Movement(self, job_routine.region_name, job_routine.ressources, job_routine.city_name)

        self.select()

        self.Fight = Fight()
        self.Inventory = Inventory()
        self.Craft = Craft(craft_names=job_routine.crafts, max_pods=self.max_pods)
        self.Scanner = Scanner(self, job_routine.ressources)

        if Positions.WINDOW_SIZE_PERC <= 0.5:
            Bot.CONFIDENCE = 0.7

    def select(self):
        CurrentBot.id = self.id
        CurrentBot.location = self.Movement.location
        CurrentBot.region = self.Movement.region

        self.window.activate()
        time.sleep(0.5)

    # ==================================================================================================================
    # INITIALIZATION
    def reset(self):
        print("")
        print("=" * 50)
        print('|  RESET')
        print("=" * 50)
        print("")

        self.Movement.reset()
        ErrorHandler.reset(self.id)

        self.check_situation()

    def reset_routine(self):
        self.current_routine = None
        self.current_step = 0

    def check_situation(self):
        """ on reset check the situation the character is in """
        if self.Fight.check_combat_started():
            self.fight_routine()

        elif self.check_tomb():
            self.Movement.ghost_routine()

        elif check_ok_button(click=True):
            return

        elif check_is_ghost():
            self.Movement.phoenix_routine()

        elif self.check_craft():
            self.craft_routine()

        elif self.check_pods():
            self.bank_routine()

    # ==================================================================================================================
    # RUN
    def play(self):
        self.select()

        # if last_position set : check map changed
        if self.Movement.last_location is not None:
            success = check_map_change(self.Movement.last_location, at_time=self.Movement.last_time_requested_movement)
            if success:
                self.Movement.last_location = None
                self.Movement.location = read_map_location()
                print(f'     location : {self.Movement.location}')
                print("")
            elif self.Fight.check_combat_started():
                return self.fight_routine()
            elif self.Movement.last_time_requested_movement is None or time.time() - self.Movement.last_time_requested_movement < ErrorHandler.TRAVEL_MAP_TIME:
                return

        # check if has craft order
        if self.check_craft():
            self.craft_routine()
            return

        if self.current_routine == Routines.Bank:
            return self.bank_routine()
        elif self.current_routine == Routines.Craft:
            return self.craft_routine()
        elif self.current_routine == Routines.Fight:
            return
        elif self.current_routine == Routines.Ghost:
            return self.Movement.ghost_routine()
        elif self.current_routine == Routines.Phoenix:
            return self.Movement.phoenix_routine()

        elif self.current_routine is None:
            # check if character needs to go unload ressources to the bank
            if self.check_pods():
                return self.bank_routine()

            if self.Movement.location in self.Movement.path:
                # scan for ressources
                done = self.Scanner.scan()
                if not done:
                    return

                if ErrorHandler.is_error:
                    return

                # check if fight has occurred
                time.sleep(1)
                if self.Fight.check_combat_started():
                    return self.fight_routine()

            self.Movement.go_to_next_location()

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

        self.Movement.current_path_index = 0
        if self.check_tomb():
            self.Movement.ghost_routine()

        elif self.Fight.check_is_defeat():
            self.on_death()

    def bank_routine(self, unload_ressources: (str, List[str]) = None):
        """ go to the bank and unload ressources """
        bank = self.Movement.city.bank

        # --------------------------------------------------------
        # STEP 0 : init routine
        if self.current_routine != Routines.Bank or self.current_step == 0:
            print("-- bank routine")
            self.current_routine = Routines.Bank
            self.current_step = 1

        # --------------------------------------------------------
        # STEP 1 : go to the bank
        if self.current_step == 1:
            done = self.Movement.move_towards(bank.LOCATION)
            if not done:
                return

            print("Clicking on BANK_DOOR")
            if not bank.enter():
                return

            Sleeper.sleep(1)
            self.current_step += 1
            return

        # --------------------------------------------------------
        # STEP 2 : open bank - unload - exit
        elif self.current_step == 2:
            if ErrorHandler.is_error:
                return

            # unload ressources in bank
            bank.open()
            time.sleep(1)

            # unload ressources in bank
            bank.unload_ressources()

            if unload_ressources is  None:
                unload_ressources = []

            unload_ressources += self.unload_ressources
            if len(unload_ressources) is not None:
                if isinstance(unload_ressources, str):
                    unload_ressources = [unload_ressources]

                for ressource_name in unload_ressources:
                    success = bank.transfer(ressource_name, from_bank=False)
                    if not success:
                        ErrorHandler.warning(f"unable to transfer {ressource_name}")

            # reset unload ressource
            self.unload_ressources = []

            # transfer ressources for requested crafts if possible (success -> craft order is set)
            self.Craft.transfer_required_ressources()

            # close bank tab
            bank.close()

            # get out of the bank
            bank.exit()

            self.reset_routine()

    def craft_routine(self):
        if self.Craft.craft_order is None:
            ErrorHandler.error("Call for craft routine when craft_order is None")
            ErrorHandler.is_error = True

        if self.Craft.is_crafting is False:
            ErrorHandler.error("Call for craft routine when craft_order is None")
            ErrorHandler.is_error = True

        # init job/building
        job = self.Craft.get_job(self.Craft.craft_order)
        building = self.Movement.city.get_craft_building(job)

        # ---------------------------------------------------
        # STEP 0 : init routine
        if self.current_routine != Routines.Craft or self.current_step == 0:
            print("-- craft routine")
            self.current_routine = Routines.Craft
            self.current_step = 1

        # ---------------------------------------------------
        # STEP 1 : go to building
        if self.current_step == 1:
            # go to the craft building
            done = self.Movement.move_towards(building.LOCATION)
            if not done:
                return

            self.current_step += 1

        # ---------------------------------------------------
        # STEP 2 : enter the building
        if self.current_step == 2:
            # enter the requested building for the craft
            building.enter()
            Sleeper.sleep(5)
            self.current_step += 1
            return

        # ---------------------------------------------------
        # STEP 3 : do the craft - exit - start the bank routine
        if self.current_step == 3:
            # craft the requested ordered
            building.use_machine()
            building.craft(self.Craft.craft_order)
            building.exit_machine()

            time.sleep(1)

            # exit building
            building.exit()

            # go to bank to unload
            self.unload_ressources.append(self.Craft.craft_order)
            self.Craft.craft_order = None
            self.bank_routine()

    # ==================================================================================================================
    # FIGHT
    @staticmethod
    def join_fight():
        wait_click_on(Images.JOIN_FIGHT_IMG)

    def on_death(self):
        check_ok_button(True)
        time.sleep(2)

        self.Movement.location = read_map_location()

        wait_click_on(Images.CANCEL_POPUP, confidence=0.7)

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