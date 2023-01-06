from typing import List

import pyautogui

from src.Bot import Bot
from src.enum.images import Images
from src.utils.ErrorHandler import ErrorHandler
from src.utils.utils_fct import wait_click_on, wait_image


class BotManager:
    """ Handle all Bots """
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
    def __init__(self, region_name):
        self.bots: List[Bot] = []

        self.create_bots(region_name)

    def create_bots(self, region_name):
        # get only dofus windows
        all_windows = pyautogui.getAllWindows()
        for window in all_windows:
            if "Dofus" in window.title:
                self.bots.append(Bot(
                    region_name=region_name,
                    ressources=[],
                    window=window
                ))

    # ==================================================================================================
    # MAIN
    def run(self):
        for bot in self.bots:
            bot.play()

    def fight_routine(self):
        while True:
            fight_started = self.bots[0].scan()
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
