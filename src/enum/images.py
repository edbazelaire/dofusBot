import math
import os
from PIL import Image

from src.enum.positions import Positions
from src.utils.ErrorHandler import ErrorHandler


class Images:
    IMAGES_DIR = 'images'

    # COMMONS               ====================================================================
    SCREENSHOTS_DIR = 'screenshots'
    PHOENIX_STATUE = 'phoenix_statue.png'
    PHOENIX_STATUE_2 = 'phoenix_statue_2.png'
    PHOENIX_STATUE_3 = 'phoenix_statue_3.png'
    YES_BUTTON = 'yes_button.png'
    CURSOR_LEFT = 'cursor_left.png'
    CURSOR_RIGHT = 'cursor_right.png'
    CURSOR_UP = 'cursor_up.png'
    CURSOR_DOWN = 'cursor_down.png'
    GHOST_FORM = 'ghost_form.png'                                   # TODO
    OK_TRANSFER_BUTTON = 'ok_transfer.png'
    INVENTORY_OPENED = 'inventory_opened.png'
    CRAFT_MACHINE_LOADED = 'craft_machine_loaded.png'

    # BANK                  ====================================================================
    BANK_DIR = 'bank'
    BANK_NPC_ASTRUB = 'bank_npc.png'
    BANK_NPC_BONTA = 'bank_npc_bonta.png'
    BANK_DIALOG_ACCESS = 'dialog_access_bank_button.png'
    BANK_ALL_TAB = 'bank_all_tab.png'
    BANK_ITEM_TAB = 'bank_item_tab.png'
    BANK_CONSUMABLE_TAB = 'bank_consumable_tab.png'
    BANK_RESSOURCE_TAB = 'bank_ressource_tab.png'
    BANK_PLAYER_TRANSFER_BUTTON = 'bank_player_transfer_button.png'
    BANK_TRANSFER_BUTTON = 'bank_transfer_button.png'
    BANK_TRANSFER_VISIBLE_OBJ_BTN = 'transfer_visible_ressources_button.png'
    BANK_OPEN = 'bank_open.png'     # TODO : image that validates that bank is open or no
    RECIPES_OPEN = 'recipes_open.png'

    # STUFFS                ====================================================================
    STUFFS_DIR = 'stuffs'
    FIGHT_STUFF = 'fight_stuff.png'
    PODS_STUFF = 'pods_stuff.png'

    # QUICK INVENTORY       ====================================================================
    QUICK_INV_DIR = 'quick_inv'
    BONTA_POTION = 'bonta_potion.png'
    RECALL_POTION = 'recall_potion.png'

    # FIGHT                 ====================================================================
    FIGHT_DIR = 'fight'
    READY_BUTTON = 'ready.png'
    END_TURN_BUTTON = 'end_turn.png'
    FF_BUTTON = 'ff_button.png'
    OK_FF_BUTTON = 'ok_ff.png'
    VICTORY = 'victory.png'
    DEFEAT = 'defeat.png'
    CANCEL_POPUP = 'cancel_popup.png'

    ENEMIES_DIR = 'enemies'
    CHAR_DIR = 'char'

    @staticmethod
    def get(img: str):
        # check if already has path
        if img.startswith(Images.IMAGES_DIR + '/'):
            return Images.load(img_path=img)

        # else find image in images dir
        for r, d, f in os.walk(Images.IMAGES_DIR):
            for filename in f:
                if filename.lower() == img.lower():
                    return Images.load(os.path.join(r, filename))

        ErrorHandler.fatal_error('unkown image ' + img)

    @staticmethod
    def load(img_path: str):
        img = Image.open(img_path)
        return img.resize((
            math.floor(img.size[0] * Positions.WINDOW_SIZE_PERC),
            math.floor(img.size[1] * Positions.WINDOW_SIZE_PERC),
        ))

    @staticmethod
    def get_enemy_images():
        base_dir = Images.IMAGES_DIR + '/' + Images.FIGHT_DIR + '/' + Images.ENEMIES_DIR
        return [base_dir + '/' + filename for filename in os.listdir(base_dir)]

    @staticmethod
    def get_char_images():
        base_dir = Images.IMAGES_DIR + '/' + Images.FIGHT_DIR + '/' + Images.CHAR_DIR
        return [base_dir + '/' + filename for filename in os.listdir(base_dir)]

    @staticmethod
    def change_color(img, min_value=210):
        """ not implemented yet, keep only white in the image """
        height, width = img.size
        image_data = img.load()

        for loop1 in range(height):
            for loop2 in range(width):
                r, g, b = image_data[loop1, loop2]
                if r <= min_value or g <= min_value or b <= min_value:
                    image_data[loop1, loop2] = 0, 0, 0
                else:
                    image_data[loop1, loop2] = 255, 255, 255

        return img