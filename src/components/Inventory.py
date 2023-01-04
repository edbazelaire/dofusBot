import time
import pyautogui as pg
import pytesseract

from src.enum.images import Images
from src.enum.positions import Positions
from src.utils.ErrorHandler import ErrorHandler
from src.utils.utils_fct import wait_image


class Inventory:
    CHECK_PODS_INTERVAL = 5 * 60

    last_time_check_pods = None

    @staticmethod
    def get_max_pods() -> int:
        """ read max pods from inventory """
        Inventory.open()

        pg.moveTo(*Positions.INVENTORY_PODS_BAR_MIDDLE, 1)
        time.sleep(1.5)
        img = pg.screenshot(region=Positions.INVENTORY_PODS_VALUE_REG)

        pods = pytesseract.image_to_string(img, config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')

        Inventory.close()

        if pods is None or pods == '':
            ErrorHandler.error(f"unable to read pods : {pods}")
            return 0

        return int(pods)

    @staticmethod
    def open() -> bool:
        if not Inventory.is_opened():
            pg.click(*Positions.INVENTORY_CLICK_POS)
            return Inventory.is_opened(max_timer=5)
        return True

    @staticmethod
    def close():
        if Inventory.is_opened():
            pg.click(*Positions.INVENTORY_CLICK_POS)
            for i in range(5):
                time.sleep(1)
                if not Inventory.is_opened(max_timer=1):
                    return True

            return False

        return True

    @staticmethod
    def is_opened(max_timer=2) -> bool:
        return wait_image(Images.INVENTORY_OPENED, max_timer=max_timer)

    @staticmethod
    def check_pods():
        test = False

        # open inventory
        Inventory.open()
        time.sleep(1)

        # check color at the end of the pods bar
        img = pg.screenshot(region=Positions.INVENTORY_PODS_REG)
        height, width = img.size
        image_data = img.load()
        min_value = 100

        for loop1 in range(height):
            for loop2 in range(width):
                r, g, b = image_data[loop1, loop2]
                if r >= min_value or g >= min_value or b >= min_value:
                    test = True
                    break

            if test:
                break

        # close inventory
        Inventory.close()
        time.sleep(1)

        return test