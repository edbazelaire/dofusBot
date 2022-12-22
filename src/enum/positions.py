import math
import win32gui

from src.utils.ErrorHandler import ErrorHandler


class Positions:
    """ contains all screen positions """

    ### DO NOT CHANGE ###
    WINDOW_DEFAULT_POS = [-8, -8]           # default screen position
    WINDOW_DEFAULT_SIZE = [1936, 1056]      # size of the default screen, on which the positions where calculated
    ### DO NOT CHANGE ###

    # ==================================================================================================================
    # GAME WINDOW SCREEN CONFIGURATION
    WINDOW_POS = [0, 0]         # base position (in pixels) of the game window for this screen
    WINDOW_SIZE = [0, 0]        # size of the game window for this screen
    WINDOW_POS_OFFSET = [0, 0]  # offset to add to compensate the window position from default (WINDOW_DEFAULT_POS)
    WINDOW_SIZE_PERC = [1, 1]   # percentage of size changes from default size (WINDOW_DEFAULT_SIZE)

    # ==================================================================================================================
    # GAME WINDOW
    X_MIN = 360
    X_MAX = 1560
    Y_MIN = 45
    Y_MAX = 900
    WINDOW_REG = (X_MIN, Y_MIN, X_MAX - X_MIN, Y_MAX - Y_MIN)

    # CHANGE MAP
    X_BAND_OFFSET = 20
    Y_BAND_OFFSET = 15
    CHANGE_MAP_LEFT_POS = (X_MIN - X_BAND_OFFSET, 450)
    CHANGE_MAP_RIGHT_POS = (X_MAX + X_BAND_OFFSET, 450)
    CHANGE_MAP_UP_POS = (1000, Y_MIN - Y_BAND_OFFSET)
    CHANGE_MAP_DOWN_POS = (1000, Y_MAX + Y_BAND_OFFSET)

    # ==================================================================================================================
    # BANK
    BANK_DOOR_POSITION = (1145, 343)                    # position to click in order to enter the bank
    BANK_PLAYER_INVENTORY_REG = (1241, 96, 345, 800)    # region of the player's inventory when the bank is opened
    BANK_BANK_INVENTORY_REG = (352, 96, 345, 800)       # region of the bank's inventory when the bank is opened
    BANK_PLAYER_RESSOURCE_POS = (1464, 155)             # button to click to open the ressources part of the player inventory
    BANK_BANK_RESSOURCE_POS = (578, 155)                # button to click to open the ressources part of the player inventory
    CLOSE_BANK_BUTTON_POSITION = (1564, 111)            # position of closing bank button
    GET_OUT_BANK_POSITION = (735, 710)                  # position to click to get out of the bank

    # PERSONAL TABS
    INVENTORY_CLICK_POS = (1412, 949)                   # position to click to open inventory

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

            setattr(self, name, self.resize(val))

        # update GameWindow X & Y from WindowRegion
        self.X_MIN = self.WINDOW_REG[0]
        self.Y_MIN = self.WINDOW_REG[1]
        self.X_MAX = self.X_MIN + self.WINDOW_REG[2]
        self.Y_MAX = self.Y_MAX + self.WINDOW_REG[3]

    @staticmethod
    def resize(pos: tuple):
        x = math.floor(pos[0] / Positions.WINDOW_SIZE_PERC[0]) + Positions.WINDOW_POS_OFFSET[0]
        y = math.floor(pos[1] / Positions.WINDOW_SIZE_PERC[1]) + Positions.WINDOW_POS_OFFSET[1]

        if len(pos) == 2:
            new_val = (x, y)
        elif len(pos) == 4:
            reg_size_x = math.floor(pos[2] / Positions.WINDOW_SIZE_PERC[0])
            reg_size_y = math.floor(pos[3] / Positions.WINDOW_SIZE_PERC[1])
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
        def callback(hwnd, extra):
            name = win32gui.GetWindowText(hwnd)
            if 'Dofus' not in name or Positions.WINDOW_SIZE != [0, 0]:
                return

            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            size_x = rect[2] - x
            size_y = rect[3] - y
            print("Window %s:" % win32gui.GetWindowText(hwnd))
            print("\tLocation: (%d, %d)" % (x, y))
            print("\t    Size: (%d, %d)" % (size_x, size_y))

            Positions.WINDOW_POS = [x, y]
            Positions.WINDOW_SIZE = [size_x, size_y]

            Positions.WINDOW_POS_OFFSET = [x - Positions.WINDOW_DEFAULT_POS[0], y - Positions.WINDOW_DEFAULT_POS[1]]
            Positions.WINDOW_SIZE_PERC = [size_x / Positions.WINDOW_DEFAULT_SIZE[0], size_y / Positions.WINDOW_DEFAULT_SIZE[1]]

        win32gui.EnumWindows(callback, None)

        if Positions.WINDOW_SIZE == [0, 0]:
            ErrorHandler.fatal_error("unable to find dofus window")

        return