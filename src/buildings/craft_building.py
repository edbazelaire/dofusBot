import time
import pyautogui as pg

from src.buildings.abstract_building import AbstractBuilding
from src.enum.images import Images
from src.enum.positions import Positions
from src.enum.ressources import Ressources
from src.utils.utils_fct import wait_click_on


class CraftBuilding(AbstractBuilding):
    def __init__(self, location, door_position, exit_position, machine_position):
        super().__init__(location, door_position, exit_position)

        self.MACHINE_POSITION = Positions.resize(machine_position)

    def use_machine(self):
        pg.click(*self.MACHINE_POSITION)
        time.sleep(3)

    def craft(self, craft_name):
        # search craft in the recipes
        ressource = Ressources.get(craft_name)
        pg.click(*Positions.CRAFT_SEARCH_BAR)
        pg.typewrite(ressource.name, interval=0.1)
        time.sleep(2)

        # select craft
        pg.doubleClick(*Positions.CRAFT_FIRST_SLOT)
        time.sleep(1)

        # select max quantity
        pg.click(*Positions.CRAFT_QUANTITY_BTN)
        time.sleep(1)

        # validate
        pg.press('enter')
        time.sleep(1)

        # craft
        pg.click(*Positions.CRAFT_FUSION_BTN)
        time.sleep(1)

    def exit_machine(self):
        pg.click(*Positions.CRAFT_EXIT_MACHINE_BTN)
        time.sleep(1)
