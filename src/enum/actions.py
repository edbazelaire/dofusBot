from src.enum.images import Images
from src.enum.locations import Locations
from src.utils.ErrorHandler import ErrorHandler

import pyautogui as pg
import time

from src.utils.utils_fct import read_map_location, check_map_change


class Actions:
    TAKE_BONTA_POTION = 'take_bonta_potion'
    TAKE_RECALL_POTION = 'take_recall_potion'
    EQUIP_FIGHT_STUFF = 'equip_fight_stuff'
    EQUIP_PODS_STUFF = 'equip_pods_stuff'

    CLICK_ON = 'click_on'
    WAIT = 'wait'

    @staticmethod
    def is_action(value: str):
        if isinstance(value, str):
            for name, val in vars(Actions).items():
                if val == value:
                    return True

        elif isinstance(value, list):
            if Actions.is_action(value[0]):
                return True

        return False

    # __________________________________________________________________________________________________________________
    @staticmethod
    def do(action: (list, str), *args):
        if not Actions.is_action(action):
            ErrorHandler.fatal_error(f"requested action ({action}) is not an action")
            return

        # LIST (action with args)
        if isinstance(action, list):
            Actions.do(action[0], *action[1:])

        # DRINK POTIONS
        elif action == Actions.TAKE_BONTA_POTION:
            Actions.take_potion(img=Images.BONTA_POTION, expected_location=Locations.BONTA_MILICE_LOCATION)

        elif action == Actions.TAKE_RECALL_POTION:
            Actions.take_potion(img=Images.RECALL_POTION)

        # EQUIP STUF
        elif action == Actions.EQUIP_FIGHT_STUFF:
            Actions.equip_stuff(Images.FIGHT_STUFF)

        elif action == Actions.EQUIP_PODS_STUFF:
            Actions.equip_stuff(Images.PODS_STUFF)

        elif action == Actions.CLICK_ON:
            Actions.click_on(args[0])

        else:
            ErrorHandler.fatal_error(f"not implemented action {action}")

    # __________________________________________________________________________________________________________________
    @staticmethod
    def take_potion(img: str, expected_location: list = None, offset_x=5, offset_y=5) -> bool:
        # to check with ocr that map was loaded
        current_location = read_map_location()

        pos = None
        start = time.time()
        while pos is None:
            if time.time() - start >= 5:
                ErrorHandler.error("unable to find potion")
                ErrorHandler.is_error = True
                return False
            pos = pg.locateOnScreen(Images.get(img), confidence=0.8)

        # use potion
        pg.doubleClick(pos[0] + offset_x, pos[1] + offset_y)

        # wait until map is loaded
        check_map_change(from_location=current_location)

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
            pos = pg.locateOnScreen(Images.get(img), confidence=0.7)

        pg.doubleClick(pos[0] + offset_x, pos[1] + offset_y)

    # __________________________________________________________________________________________________________________
    @staticmethod
    def click_on(pos):
        pg.click(pos[0], pos[1])

    # __________________________________________________________________________________________________________________
    @staticmethod
    def wait(n):
        time.sleep(n)
