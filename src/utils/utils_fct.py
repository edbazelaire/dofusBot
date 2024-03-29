import math
import time
import pyautogui as pg
import pytesseract
from PIL import Image

from src.enum.images import Images
from src.enum.positions import Positions
from src.utils.Displayer import Displayer
from src.utils.ErrorHandler import ErrorHandler, ErrorType


def wait_click_on(image: (str, Image), confidence: float = 0.8, region=None, max_timer: float = 5, offset_x=None, offset_y=None) -> bool:
    if isinstance(image, str):
        image = Images.get(image)

    if region is None:
        region = Positions.WINDOW_REG

    pos = None
    start = time.time()
    while pos is None:
        if time.time() - start >= max_timer:
            return False

        pos = pg.locateOnScreen(image, confidence=confidence, region=region)

    if offset_x is None:
        offset_x = math.floor(pos.width / 2)
    if offset_y is None:
        offset_y = math.floor(pos.height / 2)

    pg.click(pos[0] + offset_x, pos[1] + offset_y)
    return True


def wait_image(image: str, confidence: float = 0.8, region=None, max_timer: float = 5):
    if isinstance(image, str):
        image = Images.get(image)

    if region is None:
        region = Positions.WINDOW_REG

    pos = None
    start = time.time()
    while pos is None:
        if time.time() - start >= max_timer:
            return False
        pos = pg.locateOnScreen(image, confidence=confidence, region=region)

    return True


def display_mouse():
    while True:
        print(pg.position(), end='\r')


def get_distance(pos1: list, pos2: list):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def read_map_location():
    """ get map location from GUID reading """

    while True:
        if ErrorHandler.is_error:
            return [0, 0]

        img = pg.screenshot(region=Positions.MAP_LOCATION_REG)
        img = img.resize((150, 30))
        value = pytesseract.image_to_string(img, config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789,-')

        try:
            split = value.split(',')
            x = int(split[0])
            y = int(split[1])

            if abs(x) > 100 or abs(y) > 100:
                ErrorHandler.error(f"bar position reading ({value})", ErrorType.RETRY_ACTION_ERROR)
                time.sleep(2)
            else:
                ErrorHandler.reset_error(ErrorType.RETRY_ACTION_ERROR)
                return [x, y]
        except:
            ErrorHandler.error(f"unable to read position ({value})", ErrorType.RETRY_ACTION_ERROR)
            time.sleep(2)


def send_message(name:str, message:str):
    pg.click(*Positions.MESSAGE_BAR)
    time.sleep(0.5)
    pg.typewrite(f"/w {name} {message}", 0.1)
    pg.press('enter')


def read_region():
    # read Zone
    img = pg.screenshot(region=Positions.MAP_ZONE_NAME_REG)
    img = Images.change_color(img, 210)
    value = pytesseract.image_to_string(img, config="--psm 7 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz")

    if value == '':
        ErrorHandler.error("unable to read region")
        return None

    split_val = value.split(',')
    return split_val[0], split_val[1]


def check_map_change(from_location, do_map_load_check=False, at_time=None) -> bool:
    """ check if player changed map by looking at map position """
    map_location = read_map_location()
    if from_location == map_location or map_location is None:
        if at_time is None or time.time() - at_time > ErrorHandler.TRAVEL_MAP_TIME:
            ErrorHandler.warning("MAP NOT CHANGED", ErrorType.MAP_NOT_CHANGED_ERROR)
        return False

    Displayer.print("     MAP CHANGED")
    ErrorHandler.ERROR_CTRS[ErrorType.MAP_NOT_CHANGED_ERROR] = False

    if do_map_load_check:
        check_map_loaded()
    else:
        time.sleep(1)
    return True


def check_map_loaded() -> bool:
    """ check if player changed map by looking at map position """
    start = time.time()
    while True:
        if time.time() - start > ErrorHandler.LOAD_MAP_TIME:
            Displayer.print(" -- map NOT loaded !!")
            return False

        confidence = 0.5
        pg.moveTo(*Positions.CHANGE_MAP_LEFT_POS())
        if pg.locateOnScreen(Images.get(Images.CURSOR_LEFT), region=Positions.WINDOW_REG,
                             confidence=confidence) is not None:
            Displayer.print("     -- map loaded ")
            return True

        pg.moveTo(*Positions.CHANGE_MAP_RIGHT_POS())
        if pg.locateOnScreen(Images.get(Images.CURSOR_RIGHT), region=Positions.WINDOW_REG,
                             confidence=confidence) is not None:
            Displayer.print("     -- map loaded")
            return True

        pg.moveTo(*Positions.CHANGE_MAP_UP_POS())
        if pg.locateOnScreen(Images.get(Images.CURSOR_UP), region=Positions.WINDOW_REG,
                             confidence=confidence) is not None:
            Displayer.print("     -- map loaded")
            return True

        pg.moveTo(*Positions.CHANGE_MAP_DOWN_POS())
        if pg.locateOnScreen(Images.get(Images.CURSOR_DOWN), region=Positions.WINDOW_REG,
                             confidence=confidence) is not None:
            Displayer.print("     -- map loaded")
            return True

        time.sleep(0.1)


def check_is_ghost():
    """ open inventory to check if player is in ghost form """
    # TODO
    # open_inventory()
    # success = wait_image()
    # open_inventory()
    # return success
    return False


def check_ok_button(click=False):
    """ check if there is a "ok" button popup
     :param click: if True, click the button
     """
    pos = pg.locateOnScreen(Images.get(Images.OK_BUTTON), confidence=0.6)
    if pos is None:
        return False

    pg.click(pos[0], pos[1])
    return True