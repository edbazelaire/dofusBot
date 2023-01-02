from pytesseract import pytesseract

from src.enum.images import Images
from src.enum.positions import Positions
from src.enum.ressources import Ressources
from src.utils.ErrorHandler import ErrorHandler, ErrorType
from src.utils.utils_fct import wait_click_on, wait_image, check_map_loaded

import time
import pyautogui as pg


class Bank:
    BANK_NPC_IMAGE: str = None

    def __init__(self, bank_location, bank_door_position, get_out_bank_position, bank_npc_image):
        self.BANK_LOCATION = bank_location                      # location of the bank in the city
        self.BANK_DOOR_POSITION = bank_door_position            # screen position (x, y) to click in order to get in the bank
        self.GET_OUT_BANK_POSITION = get_out_bank_position      # screen position to click to get out the bank
        self.BANK_NPC_IMAGE = bank_npc_image                    # image of the NPC in the bank to talk to

    @staticmethod
    def open():
        """ open the bank """
        # click on npc
        wait_click_on(Bank.BANK_NPC_IMAGE)

        # click on "accept" to access your bank inventory
        wait_click_on(Images.get(Images.BANK_DIALOG_ACCESS))

    @staticmethod
    def close():
        pg.click(*Positions.CLOSE_BANK_BUTTON_POSITION)

        while Bank.check_is_opened():
            ErrorHandler.error('bank not closed', ErrorType.RETRY_ACTION_ERROR)
            pg.click(*Positions.CLOSE_BANK_BUTTON_POSITION)
            time.sleep(1)

        ErrorHandler.reset_error(ErrorType.RETRY_ACTION_ERROR)
        time.sleep(1)

    def exit(self) -> bool:
        for i in range(10):
            pg.click(*self.GET_OUT_BANK_POSITION)

            time.sleep(1)
            success = check_map_loaded()
            if success:
                ErrorHandler.reset_error(ErrorType.RETRY_ACTION_ERROR)
                return True

            ErrorHandler.error("unable to get out of bank", ErrorType.RETRY_ACTION_ERROR)
            if ErrorHandler.is_error:
                return False

    # ==================================================================================================================
    # BANK TAB
    @staticmethod
    def transfer(ressource_name, n, from_bank=True) -> bool:
        """
            transfer ressource from/to the bank
        :param ressource_name:  name of the ressource to transfer
        :param n:               number to transfer
        :param from_bank:       if True, transfer FROM bank TO player. Otherwise, the opposite
        """
        if n <= 0:
            ErrorHandler.warning(f"bad transfer request quantity : {n}")
            return True

        exists = Bank.search(ressource_name, in_bank=from_bank)
        if not exists:
            return False

        # Press and hold the alt key
        pg.keyDown('alt')

        # Click the left mouse button
        if from_bank:
            pg.click(*Positions.BANK_FIRST_RESSOURCE_POSITION)
        else:
            pg.click(*Positions.BANK_PLAYER_FIRST_RESSOURCE_POSITION)

        # Release the alt key
        pg.keyUp('alt')

        # type quantity of ressources to transfer
        pg.typewrite(str(n))

        # validate transfer from bank
        if not wait_click_on(Images.get(Images.VALIDATE_TRANSFER_BUTTON)):
            ErrorHandler.error(f"Unable to transfer ressource {ressource_name} in Bank")
            return False

        return True

    @staticmethod
    def get_quantity_of(ressource_name, in_bank=True):
        """ get quantity of requested ressource in the bank """
        exists = Bank.search(ressource_name, in_bank=in_bank)
        if not exists:
            return 0

        quantity_reg = Positions.BANK_FIRST_RESSOURCE_QUANTITY_REG if in_bank else Positions.BANK_PLAYER_FIRST_RESSOURCE_QUANTITY_REG

        img = pg.screenshot(region=quantity_reg)
        img = img.resize((200, 100))
        img = Images.change_color(img, min_value=150)
        value = pytesseract.image_to_string(img, config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')

        if value is None:
            ErrorHandler.warning(f"Unable to read value {value} for ressource {ressource_name}")
            # keep error for now (debug) but when there is only 1 item, there is no quantity number so the error can happen
            return 1

        return value

    # ==================================================================================================================
    # PLAYER TAB
    @staticmethod
    def unload_ressources():
        if not Bank.check_is_opened():
            Bank.open()
            time.sleep(1)

        Bank.select_player_ressource_tab()
        time.sleep(1)

        Bank.unload_all_visible()
        time.sleep(1)

    @staticmethod
    def unload_all_visible():
        wait_click_on(Images.get(Images.BANK_TRANSFER_BUTTON), confidence=0.99)
        time.sleep(1)

        # validate ressources unloading
        wait_click_on(Images.get(Images.BANK_TRANSFER_VISIBLE_OBJ_BTN))

    @staticmethod
    def select_player_ressource_tab():
        wait_click_on(
            Images.get(Images.BANK_RESSOURCE_TAB),
            region=Positions.BANK_PLAYER_INVENTORY_REG,
            offset_x=5,
            offset_y=5,
            confidence=0.99
        )

    # ==================================================================================================================
    # UTILS
    @staticmethod
    def search(ressource_name, in_bank=True):
        if in_bank:
            search_btn_pos = Positions.BANK_SEARCH_BUTTON
            reset_btn_pos = Positions.BANK_SEARCH_BAR_RESET_BUTTON
            search_bar_pos = Positions.BANK_SEARCH_BAR
        else:
            search_btn_pos = Positions.BANK_PLAYER_SEARCH_BUTTON
            reset_btn_pos = Positions.BANK_PLAYER_SEARCH_BAR_RESET_BUTTON
            search_bar_pos = Positions.BANK_PLAYER_SEARCH_BAR

        # open search bar
        pg.click(*search_btn_pos)
        time.sleep(1)

        # reset search bar
        pg.click(*reset_btn_pos)
        time.sleep(1)

        # click on search bar
        pg.click(*search_bar_pos)
        time.sleep(1)

        # type ressource name in search bar
        ressource = Ressources.get(ressource_name)
        pg.typewrite(ressource.name)

        # if first slot empty, return false
        return not Bank.check_first_slot_empty(in_bank)

    @staticmethod
    def check_is_opened() -> bool:
        """ return True if bank is open """
        return wait_image(Images.get(Images.BANK_OPEN))

    @staticmethod
    def check_first_slot_empty(in_bank=True) -> bool:
        """ check if first slot is empty """
        pos = Positions.BANK_FIRST_RESSOURCE_POSITION if in_bank else Positions.BANK_PLAYER_FIRST_RESSOURCE_POSITION
        EXPECTED_COLOR = (0, 0, 0)  # TODO !
        CHECK_REGION = (
            pos[0] - 20,
            pos[1] - 20,
            40,
            40
        )

        img = pg.screenshot(CHECK_REGION)
        height, width = img.size
        image_data = img.load()

        for y in range(height):
            for x in range(width):
                if image_data[y, x] != EXPECTED_COLOR:
                    return False

        return True
