class Positions:
    """ contains all screen positions """

    ### DO NOT CHANGE ###
    WINDOW_DEFAULT_SIZE = [1900, 1035]       # size of the default screen, on which the positions where calculated
    ### DO NOT CHANGE ###

    # ==================================================================================================================
    # GAME WINDOW SCREEN CONFIGURATION
    WINDOW_POS = [0, 0]         # base position (in pixels) of the game window for this screen
    WINDOW_SIZE = [0, 0]        # size of the game window for this screen
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
    BANK_DOOR_POSITION = (1145, 343)            # position to click in order to enter the bank
    BANK_PLAYER_INVENTORY_REG = (1241, 96, 345, 800)              # region of the player's inventory when the bank is opened
    BANK_BANK_INVENTORY_REG = (352, 96, 345, 800)                # region of the bank's inventory when the bank is opened
    BANK_PLAYER_RESSOURCE_POS = [1464, 155]
    BANK_BANK_RESSOURCE_POS = [578, 155]
    CLOSE_BANK_BUTTON_POSITION = (1564, 111)    # position of closing bank button
    GET_OUT_BANK_POSITION = (735, 710)          # position of closing bank button

    # PERSONAL TABS
    INVENTORY_CLICK_POS = (1412, 949)           # position to click to open inventory

    # RESSOURCES
    RESSOURCE1_REG = (1218, 934, 34, 16)
    RESSOURCE2_REG = (1176, 934, 34, 16)
    RESSOURCE3_REG = (1134, 934, 34, 16)
    RESSOURCE4_REG = (1092, 934, 34, 16)
    RESSOURCES_REG = [RESSOURCE1_REG, RESSOURCE2_REG, RESSOURCE3_REG, RESSOURCE4_REG]

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

    def __init__(self, window_size):
        Positions.WINDOW_POS = window_size
