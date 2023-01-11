import time
from typing import List

import pyautogui as pg
from pytesseract import pytesseract

from data.JobRoutines import get_job_routine, CharNames, get_char_id
from src.Bot import Bot
from src.components.craft.craft import Craft
from src.enum.images import Images
from src.utils.ErrorHandler import ErrorHandler
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
    def __init__(self, teams=None, n_max=None):
        if teams is None:
            teams = []

        self.teams = teams
        self.team_index = 0
        self.bots: List[Bot] = []
        self.ankama_launcher = self.get_ankama_launcher_window()

        self.create_bots(n_max)

    @staticmethod
    def get_ankama_launcher_window():
        all_windows = pg.getAllWindows()
        for window in all_windows:
            if "Ankama Launcher" in window.title:
                return window

    def create_bots(self, n_max=None):
        # get only dofus windows
        all_windows = pg.getAllWindows()
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
                    job_routine=job_routine
                )
                self.bots.append(bot)
                ctr += 1

                if n_max is not None and ctr >= n_max:
                    return

    # ==================================================================================================
    # MAIN
    def run(self):
        while True:
            TIME_DURATION = None
            start_time = time.time()

            while True:
                if TIME_DURATION is not None and time.time() - start_time >= TIME_DURATION:
                    break

                for bot in self.bots:
                    bot.play()

                    if ErrorHandler.is_error:
                        bot.reset()

            self.finish_routines()
            self.unload_all_bank()
            self.exchange_ressources()
            self.craft_all()

            if len(self.teams) > 1:
                self.swap_team()

    # ==================================================================================================================
    # CRAFT TEAM
    def finish_routines(self):
        all_done = False
        while not all_done:
            all_done = True
            for bot in self.bots:
                if bot.current_routine is not None:
                    all_done = False
                    bot.play()

        return

    def unload_all_bank(self):
        pass

    def exchange_ressources(self):
        # take account of who needs what
        requested_ressources = {}
        available_ressources = {}

        # check who is producing and who is requesting what
        for bot in self.bots:
            requested_ressources[bot.id], available_ressources[bot.id] = bot.get_requested_and_available_ressources()

        # check who has requested ressources and start exchanges
        for bot in self.bots:
            for requested_ressource in requested_ressources[bot.id]:
                for bot_id, ressources in available_ressources.items():
                    if requested_ressource in ressources:
                        self.start_exchange(bot, self.bots[bot_id], ressources=[requested_ressource])

        return

    def craft_all(self):
        for bot in self.bots:
            continue
        return

    def swap_team(self):
        if len(self.teams) <= 1:
            return

        for bot in self.bots:
            bot.window.close()

        self.team_index = (self.team_index + 1) % len(self.teams)

        time.sleep(0.5)
        try:
            self.ankama_launcher.activate()
        except:
            pass
        wait_click_on(Images.MULTI_ACCOUNT_BUTTON, max_timer=2)

        for char_name in self.current_team:
            self.log_character(char_name)

        return

    @staticmethod
    def log_character(char_name: CharNames):
        all_avatar_pos = pg.locateAllOnScreen(Images.get(Images.ACCOUNT_AVATAR))
        for pos in all_avatar_pos:
            pseudo_pos = (pos[0] + 40, pos[1])
            img = pg.screenshot(region=(pseudo_pos[0], pseudo_pos[1], 150, 20))
            value = pytesseract.image_to_string(img, config="--psm 8 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz#0123456789")

            if get_char_id(char_name) in value:
                pg.moveTo(*pseudo_pos, 0.4)
                wait_click_on(Images.LOG_ACCOUNT)

    # ==================================================================================================================
    # EXCHANGING
    def start_exchange(self, bot1: Bot, bot2: Bot, ressources: list):

        bot1.start_exchange()

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
