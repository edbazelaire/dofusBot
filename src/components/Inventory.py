import time

from src.enum.images import Images
from src.enum.positions import Positions

import pyautogui as pg

from src.utils.utils_fct import wait_image


class Inventory:
    def __init__(self):
        self.max_pods = self.get_max_pods()

    @staticmethod
    def get_max_pods() -> int:
        Inventory.open()
        # TODO
        pods = read_pods()
        Inventory.close()

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