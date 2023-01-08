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
    def get_max_pods(debug=False) -> int:
        """ read max pods from inventory """
        Inventory.open()

        time.sleep(0.5)
        pg.moveTo(*Positions.INVENTORY_PODS_BAR_MIDDLE, 0.5)
        time.sleep(1.5)
        img = pg.screenshot(region=Positions.INVENTORY_PODS_VALUE_REG)

        pods = pytesseract.image_to_string(img, config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')

        Inventory.close()

        if pods is None or pods == '':
            ErrorHandler.error(f"unable to read pods : {pods}")
            return 0

        pods = int(pods)
        print(f"MAX PODS : {pods}")

        if debug:
            img.show()

        return pods

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
        Inventory.last_time_check_pods = time.time()

        # open inventory
        Inventory.open()

        test = wait_image(Images.FULL_PODS, max_timer=1)

        # close inventory
        Inventory.close()
        time.sleep(0.5)

        return test