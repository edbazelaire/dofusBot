from pytesseract import pytesseract

from src.enum.images import Images
from src.enum.positions import Positions

import pyautogui as pg
import time

from src.utils.ErrorHandler import ErrorHandler
from src.utils.utils_fct import wait_click_on


class Fight:
    CASE_SIZE = [80, 40]

    def __init__(self):
        self.char_images = Images.get_char_images()
        self.enemy_images = Images.get_enemy_images()

    def fight(self):
        print("COMBAT STARTED")

        self.forfait()
        return

        self.equipe_stuff(Images.FIGHT_STUFF)

        # while True:
        #     print("\n====================================================")
        #     print(f"CAN MOVE : {self.can_move()}")
        #     print(f"IS AT ENEMY CONTACT : {self.is_at_enemy_contact()}")
        #     time.sleep(2)

        while self.check_combat_started():
            self.press_ready_button()
            time.sleep(2)

        while not self.check_combat_ended():
            if not self.is_my_turn():
                time.sleep(1)
                continue

            self.play_turn()
            time.sleep(0.5)

        print("COMBAT ENDED")

        # remove "defeat" popup
        pos = pg.locateOnScreen(Images.get_fight(Images.CANCEL_POPUP), confidence=0.7)
        pg.click(pos[0] + 5, pos[1] + 5)

        self.equipe_stuff(Images.PODS_STUFF)

    @staticmethod
    def press_ready_button():
        pg.click(Positions.END_TURN_BUTTON_POS)

    # ==================================================================================================================
    # PLAY TURN
    def play_turn(self):
        self.move_to_enemy()

        time.sleep(1)
        self.end_turn()

    def move_to_enemy(self):
        while self.can_move() or self.is_at_enemy_contact():
            self_pos = self.locate_self()
            enemy_pos = self.locate_enemy()

    def can_move(self):
        img = pg.screenshot(region=Positions.PM_REG)
        img = Images.change_color(img)
        value = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456')
        return int(value) >= 1

    def is_at_enemy_contact(self):
        self_pos = self.locate_self()
        enemy_pos = self.locate_enemy()
        if enemy_pos is None or self_pos is None:
            return

        distance_x = abs(enemy_pos[0] - self_pos[0])
        distance_y = abs(enemy_pos[1] - self_pos[1])

        if distance_x > 1.5 * self.CASE_SIZE[0]:
            return False

        if distance_y > 1.5 * self.CASE_SIZE[1]:
            return False

        if distance_x < 0.3 * self.CASE_SIZE[0]:
            return False

        if distance_y < 0.3 * self.CASE_SIZE[1]:
            return False

        return True


    @staticmethod
    def end_turn():
        pos = pg.locateOnScreen(Images.get_fight(Images.END_TURN_BUTTON), confidence=0.7)
        pg.click(pos[0] + 30, pos[0] + 10)

    def locate_self(self):
        for char_img in self.char_images:
            pos = pg.locateOnScreen(char_img, confidence=0.7)
            if pos is not None:
                x = pos[0]
                y = pos[1]

                char_position = [x, y]
                print(f"Char located at pos {char_position}")
                return char_position

        ErrorHandler.error("CHAR NOT FOUND")
        return None

    def locate_enemy(self):
        for enemy_image in self.enemy_images:
            pos = pg.locateOnScreen(enemy_image, confidence=0.7)
            if pos is not None:
                x = pos[0]
                y = pos[1]

                enemy_position = [x, y]
                print(f"Enemy located at pos {enemy_position}")
                return enemy_position

        ErrorHandler.error("NO ENEMY FOUND")
        return None

    def forfait(self):
        # click ff button
        wait_click_on(Images.get_fight(Images.FF_BUTTON), confidence=0.7, offset_x=5, offset_y=5)
        time.sleep(1)

        # validate ff
        wait_click_on(Images.get_fight(Images.OK_FF_BUTTON), confidence=0.7)

    # ==================================================================================================================
    # CHECK
    def is_my_turn(self):
        img = pg.screenshot(region=Positions.IS_MY_TURN_REG)
        height, width = img.size
        image_data = img.load()
        min_value = 150

        for loop1 in range(height):
            for loop2 in range(width):
                r, g, b = image_data[loop1, loop2]
                if r >= min_value or g >= min_value or b >= min_value:
                    print("IS my turn")
                    return True
        print("NOT my turn")
        return False

    def check_combat_started(self):
        return pg.locateOnScreen(Images.get_fight(Images.READY_BUTTON), confidence=0.7) is not None

    def check_is_victory(self):
        return pg.locateOnScreen(Images.get_fight(Images.VICTORY), confidence=0.7) is not None

    def check_is_defeat(self):
        return pg.locateOnScreen(Images.get_fight(Images.DEFEAT), confidence=0.7) is not None

    def check_combat_ended(self):
        return self.check_is_defeat() or self.check_is_victory()
