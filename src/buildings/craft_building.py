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

        self.MACHINE_POSITION = machine_position
        self.USE_MACHINE_POSITION = machine_position

    def use_machine(self):
        pg.click(*self.MACHINE_POSITION)
        time.sleep(1)
        pg.click(*self.USE_MACHINE_POSITION)
        time.sleep(2)

    def craft(self, craft_name):
        # search craft in the recipes
        ressource = Ressources.get(craft_name)
        pg.click(*Positions.CRAFT_SEARCH_BAR)
        pg.typewrite(ressource.name)

        # select craft
        pg.doubleClick(*Positions.CRAFT_FIRST_SLOT)

        # select max quantity
        pg.click(*Positions.CRAFT_MAX_QUANTITY_BTN)

        # validate
        pg.click(*Positions.CRAFT_VALIDATE_BTN)

        # click ok button
        # TODO : verify
        wait_click_on(Images.OK_BUTTON, confidence=0.6)

    def exit_machine(self):
        pg.click(*Positions.CRAFT_EXIT_MACHINE_BTN)