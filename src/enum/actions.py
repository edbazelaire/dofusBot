from src.components.Movement import Movement
from src.enum.images import Images
from src.enum.locations import Locations
from src.utils.ErrorHandler import ErrorHandler

import pyautogui as pg
import time

from src.utils.utils_fct import read_map_location


class Actions:
    TAKE_BONTA_POTION = 'take_bonta_potion'
    TAKE_RECALL_POTION = 'take_recall_potion'
    EQUIP_FIGHT_STUFF = 'equip_fight_stuff'
    EQUIP_PODS_STUFF = 'equip_pods_stuff'

    @staticmethod
    def is_action(value: str):
        if not isinstance(value, str):
            return False

        for name, val in vars(Actions).iteritems():
            if not name.startswith('_') and name.upper() == name:
                continue

            if val == value:
                return True

        return False

    # __________________________________________________________________________________________________________________
    @staticmethod
    def do(action: str):
        if not Actions.is_action(action):
            ErrorHandler.fatal_error(f"requested action ({action}) is not an action")
            return

        # DRINK POTIONS
        if action == Actions.TAKE_BONTA_POTION:
            Actions.take_potion(img=Images.BONTA_POTION, expected_location=Locations.BONTA_MILICE_LOCATION)

        elif action == Actions.TAKE_RECALL_POTION:
            Actions.take_potion(img=Images.RECALL_POTION)

        # EQUIP STUF
        elif action == Actions.EQUIP_FIGHT_STUFF:
            Actions.equip_stuff(Images.FIGHT_STUFF)

        elif action == Actions.EQUIP_PODS_STUFF:
            Actions.equip_stuff(Images.PODS_STUFF)

        else:
            ErrorHandler.fatal_error(f"not implemented action {action}")

    # __________________________________________________________________________________________________________________
    @staticmethod
    def take_potion(img: str, expected_location: list = None, offset_x=5, offset_y=5) -> bool:
        pos = None
        start = time.time()
        while pos is None:
            if time.time() - start >= 5:
                ErrorHandler.error("unable to find potion")
                ErrorHandler.is_error = True
                return False
            pos = pg.locateOnScreen(Images.get_quick_inv(img), confidence=0.8)

        # to check with ocr that map was loaded
        current_location = read_map_location()

        # use potion
        pg.doubleClick(pos[0] + offset_x, pos[1] + offset_y)

        # wait until map is loaded
        Movement.check_map_change(from_location=current_location)

        # check that the map location is the expected one
        if expected_location is not None:
            location = read_map_location()
            if location != expected_location:
                ErrorHandler.error(f"current location {location} is different from expected location {expected_location}")
                return False

        return True

    # __________________________________________________________________________________________________________________
    @staticmethod
    def equip_stuff(img: str, offset_x=5, offset_y=5):
        pos = None
        start = time.time()
        while pos is None:
            if time.time() - start >= 6:
                ErrorHandler.error("unable to find stuff")
                return
            pos = pg.locateOnScreen(Images.get_stuff(img), confidence=0.7)

        pg.doubleClick(pos[0] + offset_x, pos[1] + offset_y)
