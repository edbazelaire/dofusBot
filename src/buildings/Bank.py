from pytesseract import pytesseract

from src.buildings.abstract_building import AbstractBuilding
from src.enum.images import Images
from src.enum.positions import Positions
from src.enum.ressources import Ressources, RessourceType
from src.utils.ErrorHandler import ErrorHandler, ErrorType
from src.utils.utils_fct import wait_click_on, wait_image, check_map_loaded

import time
import pyautogui as pg


class Bank(AbstractBuilding):
    NPC_IMAGE: str = None

    def __init__(self, location, door_position, exit_position, npc_image):
        super().__init__(location, door_position, exit_position)
        self.NPC_IMAGE = npc_image                      # image of the NPC in the bank to talk to

    def open(self):
        """ open the bank """
        # click on npc
        wait_click_on(self.NPC_IMAGE)

        # click on "accept" to access your bank inventory
        wait_click_on(Images.get(Images.BANK_DIALOG_ACCESS))

    def close(self):
        pg.click(*Positions.CLOSE_BANK_BUTTON_POSITION)
        time.sleep(0.2)

        while Bank.check_is_opened():
            ErrorHandler.error('bank not closed', ErrorType.RETRY_ACTION_ERROR)
            pg.click(*Positions.CLOSE_BANK_BUTTON_POSITION)
            time.sleep(1)

        ErrorHandler.reset_error(ErrorType.RETRY_ACTION_ERROR)
        time.sleep(0.2)

    def enter(self) -> bool:
        return self.enter_building(click_pos=self.DOOR_POSITION, loading_img=self.NPC_IMAGE)

    def exit(self) -> bool:
        for i in range(10):
            pg.click(*self.EXIT_POSITION)

            time.sleep(1)
            success = check_map_loaded()
            if success:
                ErrorHandler.reset_error(ErrorType.RETRY_ACTION_ERROR)
                time.sleep(1)
                return True

            ErrorHandler.error("unable to get out of bank", ErrorType.RETRY_ACTION_ERROR)
            if ErrorHandler.is_error:
                return False

    # ==================================================================================================================
    # BANK TAB
    @staticmethod
    def transfer(ressource_name, n=None, from_bank=True) -> bool:
        """
            transfer ressource from/to the bank
        :param ressource_name:  name of the ressource to transfer
        :param n:               number to transfer
        :param from_bank:       if True, transfer FROM bank TO player. Otherwise, the opposite
        """
        if n is not None and n <= 0:
            ErrorHandler.warning(f"bad transfer request quantity : {n}")
            return True

        exists = Bank.search(ressource_name, in_bank=from_bank)
        if not exists:
            return False

        # set transfer from / to the bank
        from_position = Positions.BANK_FIRST_RESSOURCE_POSITION if from_bank else Positions.BANK_PLAYER_FIRST_RESSOURCE_POSITION
        to_position = Positions.BANK_PLAYER_FIRST_RESSOURCE_POSITION if from_bank else Positions.BANK_FIRST_RESSOURCE_POSITION

        # drag ressource from inv to the other
        pg.moveTo(*from_position)
        pg.dragTo(*to_position, button='left', duration=1)

        # type quantity of ressources to transfer
        if n is not None and n > 0:
            pg.typewrite(str(n), interval=0.1)

        time.sleep(2)

        # validate transfer from bank
        pg.press('enter')
        time.sleep(1)

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
        Bank.select_player_ressource_tab()
        time.sleep(1)

        Bank.unload_all_visible()
        time.sleep(1)

    def unload(self, ressource_name: str):
        if not self.check_is_opened():
            self.open()
            time.sleep(1)

        ressource = Ressources.get(ressource_name)
        self.select_tab(RessourceType.All, in_bank=False)
        self.transfer(ressource.name)

    @staticmethod
    def unload_all_visible():
        wait_click_on(Images.get(Images.BANK_PLAYER_TRANSFER_BUTTON), confidence=0.99)
        time.sleep(1)

        # validate ressources unloading
        wait_click_on(Images.get(Images.BANK_TRANSFER_VISIBLE_OBJ_BTN))

    @staticmethod
    def select_tab(ressource_type, in_bank=True):
        image = None
        region = Positions.BANK_INVENTORY_REG if in_bank else Positions.BANK_PLAYER_INVENTORY_REG

        if ressource_type == RessourceType.All:
            image = Images.get(Images.BANK_ALL_TAB)

        elif ressource_type == RessourceType.Item:
            image = Images.get(Images.BANK_ITEM_TAB)

        elif ressource_type == RessourceType.Consumable:
            image = Images.get(Images.BANK_CONSUMABLE_TAB)

        elif ressource_type == RessourceType.Ressource:
            image = Images.get(Images.BANK_RESSOURCE_TAB)

        else:
            ErrorHandler.fatal_error(f"unknown ressource type {ressource_type}")

        wait_click_on(
            image,
            region=region,
            confidence=0.7
        )
    @staticmethod
    def select_player_ressource_tab():
        wait_click_on(
            Images.get(Images.BANK_RESSOURCE_TAB),
            region=Positions.BANK_PLAYER_INVENTORY_REG,
            offset_x=5,
            offset_y=5,
            confidence=0.99,
            max_timer=3
        )

    # ==================================================================================================================
    # RECIPES
    @staticmethod
    def search_recipe(craft_name) -> bool:
        # open recipes (if not done)
        success = Bank.open_recipes()
        if not success:
            ErrorHandler.error("unable to open recipes in bank")
            return False

        # check recipe in the search bar
        pg.click(*Positions.BANK_RECIPES_SEARCH_BAR)
        time.sleep(0.5)
        pg.typewrite(craft_name, interval=0.15)
        time.sleep(1)

        # check if transfer image is in the recipe region
        return wait_image(Images.BANK_TRANSFER_BUTTON, region=Positions.BANK_RECIPES_REG, max_timer=2)

    @staticmethod
    def transfer_recipe(n: int = 0) -> bool:
        success = wait_click_on(Images.BANK_TRANSFER_BUTTON, region=Positions.BANK_RECIPES_REG, max_timer=2)
        if not success:
            return False

        time.sleep(1)

        if n > 0:
            pg.typewrite(str(n), interval=0.1)
            time.sleep(0.5)

        pg.press('enter')

        return True

    @staticmethod
    def open_recipes():
        if not Bank.is_recipes_open(max_timer=0.5):
            pg.click(*Positions.BANK_RECIPES_BTN)
            return Bank.is_recipes_open(max_timer=5)

        return True

    @staticmethod
    def is_recipes_open(max_timer: float = 2):
        return wait_image(Images.RECIPES_OPEN, max_timer=max_timer)


    # ==================================================================================================================
    # UTILS
    @staticmethod
    def search(ressource_name, in_bank=True):
        if in_bank:
            reset_btn_pos = Positions.BANK_SEARCH_BAR_RESET_BUTTON
            search_bar_pos = Positions.BANK_SEARCH_BAR
        else:
            reset_btn_pos = Positions.BANK_PLAYER_SEARCH_BAR_RESET_BUTTON
            search_bar_pos = Positions.BANK_PLAYER_SEARCH_BAR

        # select "ALL" tab (since we are searching in the bank)
        Bank.select_tab(RessourceType.All, in_bank=in_bank)

        # reset search bar
        pg.click(*reset_btn_pos)
        time.sleep(0.5)

        # click on search bar
        pg.click(*search_bar_pos)
        time.sleep(0.5)

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
        EXPECTED_COLOR = (64, 66, 59)  # TODO !
        CHECK_REGION = (
            pos[0] - 20,
            pos[1] - 20,
            40,
            40
        )

        img = pg.screenshot(region=CHECK_REGION)
        height, width = img.size
        image_data = img.load()

        for y in range(height):
            for x in range(width):
                pixel = image_data[y, x]
                for color in range(len(pixel)):
                    if not (EXPECTED_COLOR[color] + 5 >= pixel[color] >= EXPECTED_COLOR[color] - 5):
                        return False

        return True
