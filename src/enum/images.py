import os


class Images:
    IMAGES_DIR = 'images'
    SCREENSHOTS_DIR = 'screenshots'

    BANK_DIR = 'bank'
    BANK_NPC_ASTRUB = 'bank_npc.png'
    BANK_NPC_BONTA = 'bank_npc_bonta.png'
    BANK_DIALOG_ACCESS = 'dialog_access_bank_button.png'
    BANK_INVENTORY_RESSOURCES_BUTTON = 'inventory_ressources_button.png'
    BANK_TRANSFER_BUTTON = 'bank_transfer_button.png'
    BANK_TRANSFER_VISIBLE_OBJ_BTN = 'transfer_visible_ressources_button.png'

    STUFFS_DIR = 'stuffs'
    FIGHT_STUFF = 'fight_stuff.png'
    PODS_STUFF = 'pods_stuff.png'

    QUICK_INV_DIR = 'stuffs'
    BONTA_POTION = 'bonta_potion.png'       # todo : take screenshot
    RECALL_POTION = 'recall_potion.png'     # todo : take screenshot

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
    def get_screenshot(image: str):
        return Images.IMAGES_DIR + '/' + Images.SCREENSHOTS_DIR + '/' + image

    @staticmethod
    def get_bank(image: str):
        return Images.IMAGES_DIR + '/' + Images.BANK_DIR + '/' + image

    @staticmethod
    def get_stuff(image: str):
        return Images.IMAGES_DIR + '/' + Images.STUFFS_DIR + '/' + image

    @staticmethod
    def get_quick_inv(image: str):
        return Images.IMAGES_DIR + '/' + Images.QUICK_INV_DIR + '/' + image

    @staticmethod
    def get_fight(image: str):
        return Images.IMAGES_DIR + '/' + Images.FIGHT_DIR + '/' + image

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