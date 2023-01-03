import pyautogui as pg
import time

from src.enum.positions import Positions
from src.utils.ErrorHandler import ErrorHandler, ErrorType
from src.utils.utils_fct import wait_click_on, check_map_loaded


class AbstractBuilding:
    def __init__(self, location, door_position, exit_position):
        self.LOCATION = Positions.resize(location)              # location of the building in the city
        self.DOOR_POSITION = Positions.resize(door_position)    # screen position (x, y) to click in order to enter the building
        self.EXIT_POSITION = Positions.resize(exit_position)    # screen position to click to get out the building

    def enter(self) -> bool:
        return self.enter_building(self.DOOR_POSITION)

    def exit(self) -> bool:
        for i in range(10):
            pg.click(*self.EXIT_POSITION)

            time.sleep(1)
            success = check_map_loaded()
            if success:
                ErrorHandler.reset_error(ErrorType.RETRY_ACTION_ERROR)
                return True

            ErrorHandler.error("unable to get out of bank", ErrorType.RETRY_ACTION_ERROR)
            if ErrorHandler.is_error:
                return False

    @staticmethod
    def enter_building(click_pos: tuple = None, click_img: str = None, loading_img: str = '') -> bool:
        """ Enter a building by clicking requested position
        :param click_pos:   position to click to enter the building
        :param click_img:   image to click in order to get in the building
        :param loading_img: waiting for this image to confirm map loading
        :return:
        """

        if click_pos is not None:
            pg.click(*click_pos)

        elif click_img is not None:
            wait_click_on(click_img)

        else:
            ErrorHandler.fatal_error("BAD CONFIGURATION, neither click_pos or click_img is provided")

        start = time.time()
        if loading_img != '':
            while pg.locateOnScreen(loading_img) is None:
                if time.time() - start > 5:
                    ErrorHandler.is_error = True
                    return False
                time.sleep(0.5)

        return True