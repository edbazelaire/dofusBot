import math
import os
from PIL import Image

from src.enum.positions import Positions
from src.utils.ErrorHandler import ErrorHandler


class Images:
    IMAGES_DIR = 'images'

    SCREENSHOTS_DIR = 'screenshots'
    PHOENIX_STATUE = 'phoenix_statue.png'
    PHOENIX_STATUE_2 = 'phoenix_statue_2.png'
    GHOST_FORM = 'ghost_form.png'   # TODO

    BANK_DIR = 'bank'
    BANK_NPC_ASTRUB = 'bank_npc.png'
    BANK_NPC_BONTA = 'bank_npc_bonta.png'
    BANK_DIALOG_ACCESS = 'dialog_access_bank_button.png'
    BANK_RESSOURCE_TAB = 'bank_ressource_tab.png'
    BANK_TRANSFER_BUTTON = 'bank_transfer_button.png'
    BANK_TRANSFER_VISIBLE_OBJ_BTN = 'transfer_visible_ressources_button.png'

    STUFFS_DIR = 'stuffs'
    FIGHT_STUFF = 'fight_stuff.png'
    PODS_STUFF = 'pods_stuff.png'

    QUICK_INV_DIR = 'quick_inv'
    BONTA_POTION = 'bonta_potion.png'
    RECALL_POTION = 'recall_potion.png'

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
        for r, d, f in os.walk('images'):
            for filename in f:
                if filename == img:
                    img = Image.open(os.path.join(r, filename))
                    return img.resize((
                        math.floor(img.size[0] * Positions.WINDOW_SIZE_PERC[0]),
                        math.floor(img.size[1] * Positions.WINDOW_SIZE_PERC[1]),
                    ))

        ErrorHandler.fatal_error("unkown image " + img)
        return None

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