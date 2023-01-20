import time
from typing import List

import pyautogui as pg
from pytesseract import pytesseract

from data.JobRoutines import get_job_routine, CharNames, get_char_id
from src.Bot import Bot
from src.enum.images import Images
from src.enum.positions import Positions
from src.enum.ressources import Ressources
from src.utils.ErrorHandler import ErrorHandler, ErrorType
from src.utils.Sleeper import Sleeper
from src.utils.utils_fct import wait_click_on, wait_image


class BotManager:
    """ Handle all Bots """

    @property
    def current_team(self) -> List[CharNames]:
        if len(self.teams) <= 1:
            return []
        return self.teams[self.team_index]

    @property
    def leader(self) -> Bot:
        return self.bots[0]

    @property
    def other_bots(self) -> List[Bot]:
        if len(self.bots) <= 1:
            return []
        else:
            return self.bots[1:]

    # ==================================================================================================
    # INITIALIZATION
    def __init__(self, n_max=None, duration=None, team_index=None, teams=None):
        if teams is None:
            teams = []

        self.teams = teams
        self.duration = duration
        self.team_index = team_index
        self.bots: List[Bot] = []
        self.ankama_launcher = self.get_ankama_launcher_window()

        self.create_bots(n_max)

        # if no characters currently logged : get next team
        if len(self.bots) == 0:
            self.swap_team()

    @staticmethod
    def get_ankama_launcher_window():
        return pg.getWindowsWithTitle("Ankama Launcher")[0]

    def create_bots(self, n_max=None):
        # get only dofus windows
        all_windows = pg.getWindowsWithTitle("Dofus 2.")
        ctr = 0
        self.bots = []
        for window in all_windows:
            if "Dofus 2." in window.title:
                _id = len(self.bots)
                char_name = window.title.split(' - Dofus')[0]
                job_routine = get_job_routine(char_name)
                if job_routine is None:
                    continue

                bot = Bot(
                    bot_id=_id,
                    window=window,
                    char_name=char_name,
                    job_routine=job_routine
                )

                # if team switch : make craft at the end of the farming session
                if self.duration is not None:
                    bot.Craft.is_allowed_crafting = False

                self.bots.append(bot)
                ctr += 1

                if n_max is not None and ctr >= n_max:
                    return

    # ==================================================================================================
    # MAIN
    def run(self):
        while True:
            if len(self.bots) == 0:
                ErrorHandler.fatal_error("no bots provided")

            start_time = time.time()

            while True:
                if self.duration is not None and time.time() - start_time >= self.duration:
                    break

                for bot in self.bots:
                    # if bot in "sleep" mode, go to next bot
                    if not Sleeper.check_remaining_time(bot_id=bot.id):
                        continue

                    bot.play()

                    if ErrorHandler.is_error:
                        bot.reset()

            self.finish_routines()
            self.unload_all_bank()
            self.exchange_ressources()

            if len(self.teams) > 1:
                self.swap_team()

    # ==================================================================================================================
    # CRAFT TEAM
    def finish_routines(self):
        print('='*50)
        print('finishing all routines ...')
        all_done = False
        while not all_done:
            all_done = True
            for bot in self.bots:
                if bot.current_routine is not None:
                    all_done = False
                    bot.play()

                    if ErrorHandler.is_error:
                        bot.reset()

        print('done ')
        print('='*50)
        return

    def unload_all_bank(self):
        print('='*50)
        print('unloading all to bank ...')
        for bot in self.bots:
            bot.select()
            bot.Craft.is_allowed_crafting = True    # reactivate craft if it was blocked
            bot.bank_routine()

        done = False
        while not done:
            done = True
            for bot in self.bots:
                if bot.current_routine is not None:
                    done = False
                    bot.play()

                    if ErrorHandler.is_error:
                        bot.reset()

                if bot.check_craft():
                    bot.craft_routine()

        print('done !')
        print('='*50)

    # ==================================================================================================================
    # EXCHANGING
    def exchange_ressources(self):
        print('='*50)
        print('EXCHANGING RESSOURCES')
        # take account of who needs what
        requested_ressources = {}
        available_ressources = {}

        # check who is producing and who is requesting what
        for bot in self.bots:
            requested_ressources[bot.id] = bot.get_requested_ressources()
            available_ressources[bot.id] = bot.get_available_ressources()

        # check who has requested ressources and start exchanges
        for bot_taking in self.bots:
            for requested_ressource in requested_ressources[bot_taking.id]:
                for bot_id, ressources in available_ressources.items():
                    bot_giving = self.bots[bot_id]

                    if requested_ressource in ressources:
                        self.exchange(bot_taking, bot_giving, ressource_name=requested_ressource)

        print('done !')
        print('='*50)
        return

    def exchange(self, bot_taking: Bot, bot_giving: Bot, ressource_name: str) -> bool:
        bank = bot_giving.Movement.city.bank

        if bot_taking.Movement.location != bank.LOCATION:
            ErrorHandler.error(f"bot {bot_taking.char_name} is supposed to be at bank location ({bank.LOCATION}) but is actually at ({bot_taking.Movement.location})")
            return False

        if bot_giving.Movement.location != bank.LOCATION:
            ErrorHandler.error(f"bot {bot_giving.char_name} is supposed to be at bank location ({bank.LOCATION}) but is actually at ({bot_giving.Movement.location})")
            return False

        bot_taking.select()
        if not bank.is_in():
            bank.enter()

        bot_giving.select()
        if not bank.is_in():
            bank.enter()

        while True:
            ressource = Ressources.get(ressource_name)
            # =======================================================
            # get ressources from the bank
            bot_giving.select()
            bank.open()
            has_any = bank.transfer(
                ressource_name=ressource_name,
                n=(bot_taking.max_pods - 100) // ressource.pods,
                from_bank=True
            )
            bank.close()

            if not has_any:
                break

            # -------------------------------------------------------
            # start exchange
            while not bot_taking.start_exchange(bot_giving.char_name):
                ErrorHandler.warning("unable to start exchange - retry", ErrorType.RETRY_ACTION_ERROR)
                if ErrorHandler.is_error:
                    break
            ErrorHandler.reset_error(ErrorType.RETRY_ACTION_ERROR)

            # -------------------------------------------------------
            # accept exchange
            if not bot_giving.accept_exchange(ressource_name, press_validation=False):
                break

            # -------------------------------------------------------
            # validate exchange by bots that takes
            if not bot_taking.validate_exchange():
                break

            # -------------------------------------------------------
            # validate exchange by bots that gives
            if not bot_giving.validate_exchange():
                break

            # =======================================================
            # transfer given ressources in the bank
            bot_taking.select()
            bank.open()
            bank.transfer(ressource_name, from_bank=False)
            bank.close()

        # make both bots leave the bank
        bot_taking.select()
        bank.exit()
        bot_giving.select()
        bank.exit()

    # ==================================================================================================================
    # SWAP TEAM
    def swap_team(self) -> bool:
        """ change team (if has multiple team) """
        if len(self.teams) <= 1:
            return True

        for i in range(len(self.teams)):
            print('='*50)
            print("SWAP TEAM")

            self.log_next_team()
            self.create_bots()

            if len(self.bots) > 0:
                print('done !')
                print('='*50)
                return True

        ErrorHandler.fatal_error('not able to log any team')

    def delete_all_bots(self):
        for window in pg.getWindowsWithTitle("Dofus 2."):
            window.close()

        self.bots = []

    def log_next_team(self):
        if len(self.teams) <= 1:
            return

        if self.team_index is None:
            self.team_index = 0
        else:
            self.team_index = (self.team_index + 1) % len(self.teams)

        self.delete_all_bots()

        time.sleep(0.5)

        for char_name in self.current_team:
            success = False
            while not success:
                success = self.log_character(char_name)
                if not success:
                    if self.check_server_full():
                        time.sleep(5*60)

                    else:
                        ErrorHandler.error(f"Unable to connect {char_name.value} for unknown reason - skipping")
                        # set success to True to skip
                        success = True

                    dofus_windows = pg.getWindowsWithTitle('Dofus 2.')
                    if len(dofus_windows) > 0:
                        dofus_windows[0].close()


    def log_character(self, char_name: CharNames) -> bool:
        # activate Ankama window
        try:
            self.ankama_launcher.activate()
            self.ankama_launcher.maximize()
        except Exception as e:
            ErrorHandler.warning("unable to activate ankama launcher window")
            print(e)

        # go to Multi Account tab
        if not wait_image(Images.MULTI_ACCOUNT_LOADED, max_timer=2):
            success = wait_click_on(Images.MULTI_ACCOUNT_BUTTON, max_timer=2, confidence=0.95, region=Positions.SCREEN_REG)
            if not success:
                ErrorHandler.warning("unable to click multi account btn")
                return False

            time.sleep(2)

        # check all avatars icons to see if one has the character's id next to it
        all_avatar_pos = pg.locateAllOnScreen(Images.get(Images.ACCOUNT_AVATAR))
        for pos in all_avatar_pos:
            pseudo_pos = (pos[0] + 40, pos[1])
            img = pg.screenshot(region=(pseudo_pos[0], pseudo_pos[1], 150, 20))
            value = pytesseract.image_to_string(img, config="--psm 8 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz#0123456789")

            if get_char_id(char_name) in value:
                pg.moveTo(*pseudo_pos, 0.4)
                check_region = (pseudo_pos[0], pseudo_pos[1]-10, 900, 50)
                success = wait_click_on(Images.LOG_ACCOUNT, region=check_region, confidence=0.85)
                if not success:
                    ErrorHandler.error(f"Unable to click log button for character : {char_name}")
                    return False

                success = wait_image(Images.CHAR_LOADED, max_timer=60, confidence=0.9, region=Positions.ACTIONS_BAR_REG)
                if not success:
                    ErrorHandler.error(f"Unable to log character : {char_name}")
                    return False

                return success

        ErrorHandler.error(f"Character not found : {char_name}")
        return False

    @staticmethod
    def check_server_full():
        return pg.locateOnScreen(Images.get(Images.SERVER_FULL), confidence=0.9) is not None;

    # ==================================================================================================================
    # FIGHT TEAM
    def fight_routine(self):
        while True:
            fight_started = self.bots[0].Scanner.scan()
            if fight_started:
                self.join_fight()

            else:
                self.go_to_next_location()

    def join_fight(self):
        """ make all other bots join the fight """
        if not wait_image(Images.JOIN_FIGHT_IMG):
            if not self.leader.Fight.check_combat_started():
                return
            else:
                ErrorHandler.error("fight started but other bots are unable to see it")

        for bot in self.other_bots:
            bot.join_fight()

        self.leader.Fight.press_ready_button()

    def go_to_next_location(self):
        next_location = self.leader.Movement.get_next_location()
        for bot in self.bots:
            bot.Movement.go_to(next_location)
