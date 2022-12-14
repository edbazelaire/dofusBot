class Positions:
    """ contains all screen positions """
    X_MIN = 370
    X_MAX = 1560
    Y_MIN = 45
    Y_MAX = 900

    X_BAND_OFFSET = 100
    Y_BAND_OFFSET = 15
    CHANGE_MAP_LEFT_POS = (X_MIN - X_BAND_OFFSET, 450)
    CHANGE_MAP_RIGHT_POS = (X_MAX + X_BAND_OFFSET, 450)
    CHANGE_MAP_UP_POS = (1000, Y_MIN - Y_BAND_OFFSET)
    CHANGE_MAP_DOWN_POS = (1000, Y_MAX + Y_BAND_OFFSET)

    # BANK
    BANK_DOOR_POSITION = (1145, 343)                 # position to click in order to enter the bank
    CLOSE_BANK_BUTTON_POSITION = (1564, 111)         # position of closing bank button
    GET_OUT_BANK_POSITION = (735, 710)         # position of closing bank button

    INVENTORY_POS = (1412, 949)

    RESSOURCE_REG = (1218, 934, 34, 16)
    MAP_LOCATION_REG = (0, 70, 80, 30)
    MAP_ZONE_NAME_REG = (0, 45, 320, 25)
    READY_BUTTON_REG = (1340, 950, 110, 35)

    END_TURN_BUTTON_POS = (1396, 965)
    SPELL_1_POS = (894, 953)
    SPELL_2_POS = (940, 953)
    SPELL_3_POS = (983, 953)
    IS_MY_TURN_REG = (895, 1020, 5, 2)
    PM_REG = (795, 1006, 20, 22)
    PA_REG = (744, 1010, 20, 22)
