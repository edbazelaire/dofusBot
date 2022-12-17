import time
import pyautogui as pg
import pytesseract

from src.enum.images import Images
from src.enum.positions import Positions
from src.utils.ErrorHandler import ErrorHandler


def wait_click_on(image: str, confidence: float = 0.8, region=None, max_timer: float = 5, offset_x=0, offset_y=0):
    pos = None
    start = time.time()
    while pos is None:
        if time.time() - start >= max_timer:
            return False
        if region is not None:
            pos = pg.locateOnScreen(image, confidence=confidence, region=region)
        else:
            pos = pg.locateOnScreen(image, confidence=confidence)

    pg.click(pos[0] + offset_x, pos[1] + offset_y)
    return True


def wait_image(image: str, confidence: float = 0.8, region=None, max_timer: float = 5):
    pos = None
    start = time.time()
    while pos is None:
        if time.time() - start >= max_timer:
            return False
        if region is not None:
            pos = pg.locateOnScreen(image, confidence=confidence, region=region)
        else:
            pos = pg.locateOnScreen(image, confidence=confidence)

    return True


def display_mouse():
    while True:
        print(pg.position(), end='\r')


def get_distance(pos1: list, pos2: list):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def read_map_location():
    """ get map location from GUID reading """

    img = pg.screenshot(region=Positions.MAP_LOCATION_REG)
    value = pytesseract.image_to_string(img, config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789,-')

    try:
        split = value.split(',')
        x = int(split[0])
        y = int(split[1])

        if abs(x) > 100 or abs(y) > 100:
            ErrorHandler.error(f"unable to read position ({value})")
            return None

        return [x, y]
    except:
        ErrorHandler.error(f"unable to read position ({value})")
        return None


def read_region():
    # read Zone
    img = pg.screenshot(region=Positions.MAP_ZONE_NAME_REG)
    img = Images.change_color(img, 210)
    value = pytesseract.image_to_string(img, config="-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz, -psm 7")

    if value is '':
        ErrorHandler.error("unable to read region")
        return None

    split_val = value.split(',')
    return split_val[0], split_val[1]


def check_map_change(from_location, do_map_load_check=True) -> bool:
    """ check if player changed map by looking at map position """
    start = time.time()
    map_location = read_map_location()
    while from_location == map_location or map_location is None:
        if time.time() - start > ErrorHandler.TRAVEL_MAP_TIME:
            print("WARNING !! MAP NOT CHANGED")
            return False
        time.sleep(0.5)

        map_location = read_map_location()

    print("     MAP CHANGED")

    if do_map_load_check:
        check_map_loaded()
    return True


def check_map_loaded() -> bool:
    """ check if player changed map by looking at map position """
    start = time.time()
    while True:
        if time.time() - start > ErrorHandler.LOAD_MAP_TIME:
            print(" -- map NOT loaded !!")
            return False

        confidence = 0.7
        pg.moveTo(*Positions.CHANGE_MAP_LEFT_POS)
        if pg.locateOnScreen('images/screenshots/cursor_left.png', confidence=confidence) is not None:
            print("     -- map loaded ")
            return True

        pg.moveTo(*Positions.CHANGE_MAP_RIGHT_POS)
        if pg.locateOnScreen('images/screenshots/cursor_right.png', confidence=confidence) is not None:
            print("     -- map loaded")
            return True

        pg.moveTo(*Positions.CHANGE_MAP_UP_POS)
        if pg.locateOnScreen('images/screenshots/cursor_up.png', confidence=confidence) is not None:
            print("     -- map loaded")
            return True

        pg.moveTo(*Positions.CHANGE_MAP_DOWN_POS)
        if pg.locateOnScreen('images/screenshots/cursor_down.png', confidence=confidence) is not None:
            print("     -- map loaded")
            return True

        time.sleep(0.1)


def check_is_ghost():
    """ open inventory to check if player is in ghost form """
    # TODO
    return False