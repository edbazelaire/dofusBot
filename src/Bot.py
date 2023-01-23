import random
from typing import List, Tuple
import pyautogui as pg
import time
import os
import pytesseract

from data.JobRoutines import JobRoutine
from src.buildings.Bank import Bank
from src.components.Inventory import Inventory
from src.components.Scanner import Scanner
from src.components.craft.craft import Craft
from src.enum.positions import Positions
from src.enum.images import Images
from src.components.Fight import Fight
from src.components.Movement import Movement
from src.enum.routines import Routines
from src.utils.CurrentBot import CurrentBot
from src.utils.Displayer import Displayer
from src.utils.ErrorHandler import ErrorHandler
from src.utils.Sleeper import Sleeper
from src.utils.utils_fct import read_map_location, check_is_ghost, check_ok_button, wait_click_on, check_map_change, \
    send_message, wait_image


class Bot:
    CURRENT_ID = 0
    MAX_TIME_SCANNING = 60

    def __init__(self, bot_id: int, window, char_name: str, job_routine: JobRoutine):
        self.current_routine: (None, Routines) = None
        self.current_step: int = 0

        self.id = bot_id
        self.window = window
        self.char_name = char_name
        self.job_routine = job_routine
        self.clicked_pos = []
        self.unload_ressources = []

        self.Movement = Movement(self, job_routine.region_name, job_routine.ressources, job_routine.city_name)

        self.select()

        self.max_pods = Inventory.get_max_pods()
        self.Fight = Fight()
        self.Inventory = Inventory()
        self.Craft = Craft(craft_names=job_routine.crafts, max_pods=self.max_pods)
        self.Scanner = Scanner(self, job_routine.ressources)

        self.Movement.location = read_map_location()

        if Positions.WINDOW_SIZE_PERC <= 0.5:
            Bot.CONFIDENCE = 0.7

    def select(self):
        CurrentBot.id = self.id
        CurrentBot.instance = self
        success = False
        while not success:
            self.window.activate()
            success = True
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

        # MOVEMENT REQUEST CHECK ==========================================
        # if last_position set : check map changed
        if self.Movement.last_location is not None:
            success = check_map_change(self.Movement.last_location, at_time=self.Movement.last_time_requested_movement)
            if success:
                self.Movement.last_location = None
                self.Movement.location = read_map_location()
                Displayer.print(f'     location : {self.Movement.location}')
                print("")
            elif self.Fight.check_combat_started():
                return self.fight_routine()
            elif self.Movement.last_time_requested_movement is None or time.time() - self.Movement.last_time_requested_movement < ErrorHandler.TRAVEL_MAP_TIME:
                return

        # check if has craft order
        if self.check_craft():
            self.craft_routine()
            return

        # ROUTINES ==========================================================
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

        # NORMAL MOVEMENT ====================================================
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
    # EXCHANGES
    def get_available_ressources(self):
        available_ressources = []

        # go threw each crafts to see if the bot uses the ressource
        for ressource_name in self.job_routine.ressources:
            if ressource_name not in available_ressources and self.is_ressource_available(ressource_name):
                available_ressources.append(ressource_name)

        # check if crafts are available
        for ressource_name in self.job_routine.crafts:
            if ressource_name not in available_ressources and self.is_ressource_available(ressource_name):
                available_ressources.append(ressource_name)

        return available_ressources

    def is_ressource_available(self, ressource_name: str):
        """go threw each crafts to see if the bot uses the ressource"""
        for craft_name in self.job_routine.crafts:
            recipe = Craft.get_recipe(craft_name)
            if ressource_name in recipe.keys():
                return False
        return True

    def get_requested_ressources(self):
        """check what ressources the bot needs that he cant farm himself"""
        requested_ressources = []
        for craft_name in self.job_routine.crafts:
            for requested_ressource in Craft.get_recipe(craft_name).keys():
                if requested_ressource not in self.job_routine.ressources and requested_ressource not in requested_ressources:
                    requested_ressources.append(requested_ressource)
        return requested_ressources

    def start_exchange(self, char_name: str) -> bool:
        self.select()

        pg.click(*Positions.PRIVATE_MESSAGES_FILTER)

        # send a random message to the player
        msg = ''.join(random.choice('azertyuiopqsdfghjklmwxcvbn') for i in range(random.randint(3, 15)))
        send_message(char_name, msg)

        pg.moveTo(*Positions.LAST_MESSAGE_NAME, 0.2)
        pg.click()
        if not wait_click_on(Images.EXCHANGE_BTN):
            ErrorHandler.error(f"unable to exchange with player {char_name}")
            return False

        if not wait_image(Images.WAITING_EXCHANGE_WINDOW):
            ErrorHandler.error(f"exchange sent to {char_name} but window did not pop")
            return False

        return True

    def accept_exchange(self, ressources: (str, List[str]), press_validation=False) -> bool:
        """
            accept an exchange request from another bot
        :param ressources: list of ressources to exchange
        :param press_validation: instant validate or wait for further confirmation
        """
        self.select()

        if isinstance(ressources, str):
            ressources = [ressources]

        if not wait_click_on(Images.YES_BUTTON, confidence=0.6):
            ErrorHandler.error("unable to find yes button")
            return False

        if not wait_image(Images.EXCHANGE_LOADED):
            ErrorHandler.error("Exchange not loaded")
            return False

        for ressource in ressources:
            Bank.transfer(ressource, from_bank=False)

        time.sleep(3)

        if press_validation:
            return self.validate_exchange()
        return True

    def validate_exchange(self) -> bool:
        """ validate an exchange """
        self.select()

        if not wait_click_on(Images.VALIDATE_BTN):
            ErrorHandler.error('unable to validate exchange')
            return False

        return True

    # ==================================================================================================================
    # CHECKS
    def check_pods(self):
        """ check number of pods by reading number of ressources in the quick inventory (faster than opening inventory
        but more subject to errors)"""
        if self.Inventory.last_time_check_pods is not None and time.time() - self.Inventory.last_time_check_pods < Inventory.CHECK_PODS_INTERVAL:
            return False

        return self.Inventory.check_pods()

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
                Displayer.print(value)
                img.show()

            value = 0 if value == '' else int(value)
            num_ressources += value

        if debug:
            Displayer.print(f"num_ressources : {num_ressources}")
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
            Displayer.print("-- bank routine")
            self.current_routine = Routines.Bank
            self.current_step = 1

        # --------------------------------------------------------
        # STEP 1 : go to the bank
        if self.current_step == 1:
            done = self.Movement.move_towards(bank.LOCATION)
            if not done:
                return

            Displayer.print("Clicking on BANK_DOOR")
            if not bank.enter():
                return

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
            if self.Craft.is_crafting:
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
            ErrorHandler.error("Call for craft routine when is_crafting is False")
            ErrorHandler.is_error = True

        # init job/building
        job = self.Craft.get_job(self.Craft.craft_order)
        building = self.Movement.city.get_craft_building(job)

        # ---------------------------------------------------
        # STEP 0 : init routine
        if self.current_routine != Routines.Craft or self.current_step == 0:
            Displayer.print("-- craft routine")
            self.current_routine = Routines.Craft
            self.current_step = 1

        # ---------------------------------------------------
        # STEP 1 : go to building
        if self.current_step == 1:
            # go to the craft building
            done = self.Movement.move_towards(building.LOCATION)
            if not done:
                return

            if building.enter():
                Sleeper.sleep(1)
                self.current_step += 1
            return

        # ---------------------------------------------------
        # STEP 2 : do the craft - exit - start the bank routine
        if self.current_step == 2:
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