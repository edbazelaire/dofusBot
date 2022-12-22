import math
import win32gui

from src.utils.ErrorHandler import ErrorHandler


class Positions:
    """ contains all screen positions """
    DONE = False

    ### DO NOT CHANGE ###
    WINDOW_DEFAULT_POS = [-8, -8]
    GAME_WINDOW_DEFAULT_POS = [325, 22]  # default screen position
    GAME_WINDOW_DEFAULT_SIZE = [1200, 855]  # size of the default screen, on which the positions where calculated
    ### DO NOT CHANGE ###

    # ==================================================================================================================
    # GAME WINDOW SCREEN CONFIGURATION
    WINDOW_POS_OFFSET = [0, 0]      # offset to add to compensate the window position from default (WINDOW_DEFAULT_POS)
    WINDOW_SIZE_PERC: float = 1     # percentage of size changes from default size (WINDOW_DEFAULT_SIZE)

    # ==================================================================================================================
    # GAME WINDOW
    X_MIN = 360
    X_MAX = 1560
    Y_MIN = 45
    Y_MAX = 900
    WINDOW_REG: list = []

    # CHANGE MAP
    X_BAND_OFFSET = 20
    Y_BAND_OFFSET = 15

    # ==================================================================================================================
    # BANK
    BANK_DOOR_POSITION = (1145, 343)  # position to click in order to enter the bank
    BANK_PLAYER_INVENTORY_REG = (1241, 96, 345, 800)  # region of the player's inventory when the bank is opened
    BANK_BANK_INVENTORY_REG = (352, 96, 345, 800)  # region of the bank's inventory when the bank is opened
    BANK_PLAYER_RESSOURCE_POS = (1464, 155)  # button to click to open the ressources part of the player inventory
    BANK_BANK_RESSOURCE_POS = (578, 155)  # button to click to open the ressources part of the player inventory
    CLOSE_BANK_BUTTON_POSITION = (1564, 111)  # position of closing bank button
    GET_OUT_BANK_POSITION = (735, 710)  # position to click to get out of the bank

    # PERSONAL TABS
    INVENTORY_CLICK_POS = (1412, 949)  # position to click to open inventory

    # RESSOURCES
    RESSOURCE1_REG = (1218, 934, 34, 16)
    RESSOURCE2_REG = (1176, 934, 34, 16)
    RESSOURCE3_REG = (1134, 934, 34, 16)
    RESSOURCE4_REG = (1092, 934, 34, 16)

    # LOCATION (location / zone / region...)
    MAP_LOCATION_REG = (0, 70, 100, 30)
    MAP_ZONE_NAME_REG = (0, 45, 320, 25)
    MAP_REGION_NAME_REG = (0, 45, 320, 25)

    # FIGHT
    READY_BUTTON_REG = (1340, 950, 110, 35)
    END_TURN_BUTTON_POS = (1396, 965)
    SPELL_1_POS = (894, 953)
    SPELL_2_POS = (940, 953)
    SPELL_3_POS = (983, 953)
    IS_MY_TURN_REG = (895, 1020, 5, 2)
    PM_REG = (795, 1006, 20, 22)
    PA_REG = (744, 1010, 20, 22)

    def __init__(self):
        self.set_window_size()

        for name, val in vars(Positions).items():
            # filter constants
            if name.upper() != name:
                continue

            # do not change default values
            if '_DEFAULT' in name:
                continue

            # do not change settings
            if name == 'WINDOW_SIZE_PERC' or name == 'WINDOW_POS_OFFSET' or name == 'WINDOW_SIZE' or name == 'WINDOW_POS':
                continue

            # filter
            if not isinstance(val, tuple):
                continue

            setattr(Positions, name, self.resize(val))

        # update GameWindow X & Y from WindowRegion
        self.X_MIN = self.WINDOW_REG[0]
        self.Y_MIN = self.WINDOW_REG[1]
        self.X_MAX = self.X_MIN + self.WINDOW_REG[2]
        self.Y_MAX = self.Y_MAX + self.WINDOW_REG[3]

    @staticmethod
    def resize(pos: tuple):
        x = math.floor(pos[0] * Positions.WINDOW_SIZE_PERC) + Positions.WINDOW_POS_OFFSET[0]
        y = math.floor(pos[1] * Positions.WINDOW_SIZE_PERC) + Positions.WINDOW_POS_OFFSET[1]

        if len(pos) == 2:
            new_val = (x, y)
        elif len(pos) == 4:
            reg_size_x = math.floor(pos[2] / Positions.WINDOW_SIZE_PERC)
            reg_size_y = math.floor(pos[3] / Positions.WINDOW_SIZE_PERC)
            new_val = (x, y, reg_size_x, reg_size_y)
        else:
            ErrorHandler.error(f'trying to set resize a tuple that is neither a pos nore a region {pos}')
            return pos

        return new_val

    @staticmethod
    def get_ressource_regions():
        return [Positions.RESSOURCE1_REG, Positions.RESSOURCE2_REG, Positions.RESSOURCE3_REG, Positions.RESSOURCE4_REG]

    @staticmethod
    def set_window_size():
        def check_game_window_size(x, y, size_x, size_y):
            import pyautogui as pg

            x_start = None
            x_end = None
            y_start = None
            y_end = None

            # CALCULATE X_START, X_END
            width_screenshot = pg.screenshot(region=(x, y + size_y/2, size_x, 20))
            width, height = width_screenshot.size
            image_data = width_screenshot.load()
            for i in range(width):
                is_black = True

                # check that all pixels of the column are black
                for j in range(height):
                    r, g, b = image_data[i, j]
                    if r > 0 or g > 0 or b > 0:
                        is_black = False
                        break

                # first column of none black pixels is x_start
                if not is_black and x_start is None:
                    x_start = x + i

                # first column of black pixels after x_start is x_end
                if is_black and x_start is not None:
                    x_end = x + i
                    break

                # if no black at the start : no offset
                if i == 0 and not is_black:
                    x_start = x
                    x_end = x + size_x

            # CALCULATE Y_START, Y_END
            height_screenshot = pg.screenshot(region=(x + size_x / 2, y, 20, size_y))
            width, height = height_screenshot.size
            image_data = height_screenshot.load()
            for j in range(height):
                is_black = True

                # check that all pixels of the row are black
                for i in range(width):
                    r, g, b = image_data[i, j]
                    if r > 0 or g > 0 or b > 0 and not (r,g,b) == (255, 255, 255):
                        is_black = False
                        break

                # first column of none black pixels is x_start
                if not is_black and y_start is None:
                    y_start = y + j

                # first column of black pixels after x_start is x_end
                if is_black and y_start is not None:
                    y_end = y + j
                    break

                # if no black at the start : no offset
                if j == 0 and not is_black:
                    y_start = y
                    y_end = y + size_y

            if None in [x_start, x_end, y_start, y_end]:
                ErrorHandler.fatal_error('unable to calculate game window dimension')

            return [x_start, y_start, x_end - x_start, y_end - y_start]

        def callback(hwnd, extra):
            name = win32gui.GetWindowText(hwnd)
            if 'Dofus' not in name or Positions.DONE:
                return

            # get size of the ALL window
            rect = win32gui.GetWindowRect(hwnd)
            window_x = rect[0] + 8
            window_y = rect[1] + 30        # add 30px because of window tab
            size_x = rect[2] - window_x - 8
            size_y = rect[3] - window_y - 8

            # get size of the GAME WINDOW
            Positions.WINDOW_REG = check_game_window_size(window_x, window_y, size_x, size_y)

            # set RELATIVE VALUES
            Positions.WINDOW_SIZE_PERC = Positions.WINDOW_REG[2] / Positions.GAME_WINDOW_DEFAULT_SIZE[0]

            Positions.WINDOW_POS_OFFSET = [
                Positions.WINDOW_REG[0] - Positions.GAME_WINDOW_DEFAULT_POS[0],
                Positions.WINDOW_REG[1] - Positions.GAME_WINDOW_DEFAULT_POS[1]
            ]

            # adjust size_y
            Positions.WINDOW_REG[3] = math.floor(Positions.WINDOW_SIZE_PERC * Positions.GAME_WINDOW_DEFAULT_SIZE[1])

            print("Window %s:" % win32gui.GetWindowText(hwnd))
            print("\tWindow Location:   (%d, %d)" % (Positions.WINDOW_REG[0], Positions.WINDOW_REG[1]))
            print("\tGame Window Size:  (%d, %d)" % (Positions.WINDOW_REG[2], Positions.WINDOW_REG[3]))

            Positions.DONE = True

        win32gui.EnumWindows(callback, None)
        if not Positions.DONE:
            ErrorHandler.fatal_error("positions not recalculated")

        return

    @staticmethod
    def CHANGE_MAP_LEFT_POS() -> tuple:
        return Positions.WINDOW_REG[0] + Positions.X_BAND_OFFSET / 2, Positions.WINDOW_REG[3] / 2

    @staticmethod
    def CHANGE_MAP_RIGHT_POS() -> tuple:
        return Positions.WINDOW_REG[0] + Positions.WINDOW_REG[2] - Positions.X_BAND_OFFSET / 2, Positions.WINDOW_REG[3] / 2

    @staticmethod
    def CHANGE_MAP_UP_POS() -> tuple:
        return Positions.WINDOW_REG[2] / 2, Positions.WINDOW_REG[1] + Positions.Y_BAND_OFFSET / 2

    @staticmethod
    def CHANGE_MAP_DOWN_POS() -> tuple:
        return Positions.WINDOW_REG[2] / 2, Positions.WINDOW_REG[1] + Positions.WINDOW_REG[3] - Positions.Y_BAND_OFFSET / 2
