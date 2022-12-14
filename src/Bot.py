import pyautogui as pg
import time
import os
import pytesseract

from src.components.Fight import Fight
from src.enum import Positions, Images, Locations
from src.components.Movement import Movement
from src.utils.ErrorHandler import ErrorHandler


class Bot:
    MAX_TIME_SCANNING = 60
    HARVEST_TIME = 1
    CONFIDENCE = 0.65
    MAX_ALLOWED_RESSOURCES = 2600

    DEATH_MAP_LOCATION = (6, -19)
    BANK_LOCATION = (4, -18)
    GATES_LOCATION = (4, -22)

    def __init__(self, ressources: list):
        self.images = {}

        self.ressources = ressources
        self.get_images(ressources)

        self.clicked_pos = []

        self.Movement = Movement(ressources)
        self.Fight = Fight()

    # ==================================================================================================================
    # INITIALIZATION
    def reset(self):
        print("")
        print("=" * 50)
        print('|  RESET')
        print("=" * 50)
        print("")

        self.clicked_pos = []
        self.Movement.reset()
        ErrorHandler.reset()

        self.make_first_move()

    def make_first_move(self):
        if self.check_pods():
            self.bank_routine()
        else:
            self.Movement.go_to_next_pos()

    def get_images(self, ressources: list):
        """ get only images of requested ressources """
        dir = 'images'
        for ressource_name in self.ressources:
            self.images[ressource_name] = [dir + '/' + filename for filename in os.listdir(dir) if filename.startswith(ressource_name)]

    # ==================================================================================================================
    # RUN
    def run(self):
        print(f"STARTING POSITION : {self.Movement.position}")
        print(f"STARTING MAP INDEX : {self.Movement.current_map_index}")

        self.make_first_move()

        while True:
            if ErrorHandler.is_error:
                self.reset()

            # scan for ressources
            self.scan()

            if ErrorHandler.is_error:
                continue

            # check if fight has occurred
            if self.Fight.check_combat_started():
                self.Fight.fight()
                if self.Fight.check_is_victory():
                    continue

                if self.check_is_ghost():
                    self.ghost_routine()
                elif self.Fight.check_is_defeat():
                    self.on_death()
                continue

            if ErrorHandler.is_error:
                continue

            # check if character needs to go unload ressources to the bank
            if self.check_pods():
                self.bank_routine()
                continue

            if ErrorHandler.is_error:
                continue

            # go to next map
            self.Movement.get_next_position()
            self.Movement.go_to_next_pos()

    def scan(self):
        print('Scanning....')
        print("")

        if self.Movement.position not in self.Movement.maps:
            ErrorHandler.error('current scanning position not in requested scanned maps')
            ErrorHandler.is_error = True

        start = time.time()
        isAny = True
        while isAny:
            isAny = self.check_all_ressources()
            if not isAny or time.time() - start > self.MAX_TIME_SCANNING:
                break
            time.sleep(self.HARVEST_TIME)

    def check_all_ressources(self):
        for name, images in self.images.items():
            for image in images:
                isAny = self.check_ressource(image)
                if isAny:
                    return True
        return False

    def check_ressource(self, image) -> bool:
        all_pos = list(pg.locateAllOnScreen(image, confidence=self.CONFIDENCE))

        for pos in all_pos:
            if (pos[0], pos[1]) in self.clicked_pos:
                continue

            if Positions.X_MAX > pos[0] > Positions.X_MIN and Positions.Y_MAX > pos[1] > Positions.Y_MIN:
                pg.click(pos[0], pos[1])
                self.clicked_pos.append((pos[0], pos[1]))
                pg.moveTo(10, 10)   # move mouse to prevent overs
                return True

        return False

    # ==================================================================================================================
    # GHOST
    def ghost_routine(self):
        self.Movement.position = Locations.PHOENIX_STATUE

        self.wait_click_on('images/screenshots/yes_button.png')

        # wait that map is loaded
        time.sleep(5)

        self.wait_click_on('images/screenshots/phoenix_statue.png', offset_x=20)
        self.wait_click_on(Images.get_fight(Images.CANCEL_POPUP), offset_x=5, offset_y=5)

        # wait until reaching phoenix statue
        time.sleep(5)

        self.Movement.go_to(Locations.TOP_CORNER_CITY_LOCATION)
        self.reset()

    # ==================================================================================================================
    # CHECKS
    def check_pods(self):
        img = pg.screenshot(region=Positions.RESSOURCE_REG)
        img = Images.change_color(img, min_value=140)
        value = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

        if value == '':
            return False

        return int(value) >= self.MAX_ALLOWED_RESSOURCES

    def check_is_ghost(self) -> bool:
        start = time.time()
        pos = None
        while True:
            if time.time() - start > 5:
                return False
            if pg.locateOnScreen('images/screenshots/tomb.png', confidence=0.7):
                return True

    # ==================================================================================================================
    # ACTIONS
    def bank_routine(self):
        print("MAX PODS REACHED -> Going to bank")

        # go to the bank
        self.Movement.go_to_bank()

        if ErrorHandler.is_error:
            return

        # unload ressources in the bank
        self.unload_bank()
        time.sleep(1)

        # get out of the bank
        pg.click(*Positions.GET_OUT_BANK_POSITION)
        self.Movement.check_map_change(do_map_load_check=True)

        # get back to first map location
        self.Movement.get_back_to_first_position()

        # reset
        self.reset()

    def unload_bank(self):
        # click on npc
        self.wait_click_on(Images.get_bank(Images.BANK_NPC))

        # click on "accept" to access your bank inventory
        self.wait_click_on(Images.get_bank(Images.BANK_DIALOG_ACCESS), offset_x=50, offset_y=10)
        time.sleep(0.5)

        # unload ressources
        self.wait_click_on(Images.get_bank(Images.BANK_TRANSFER_BUTTON), offset_x=5, offset_y=5, confidence=0.99)
        time.sleep(1)

        # validate ressources unloading
        self.wait_click_on(Images.get_bank(Images.BANK_TRANSFER_VISIBLE_OBJ_BTN))
        time.sleep(1)

        # close bank
        pg.click(*Positions.CLOSE_BANK_BUTTON_POSITION)

    def wait_click_on(self, image: str, confidence: float = 0.8, max_timer: float = 5, offset_x=0, offset_y=0):
        pos = None
        start = time.time()
        while pos is None:
            if time.time() - start >= max_timer:
                return False
            pos = pg.locateOnScreen(image, confidence=confidence)

        pg.click(pos[0] + offset_x, pos[1] + offset_y)
        return True

    # ==================================================================================================================
    # FIGHT


    def on_death(self):
        # move once left (because death pos is in building)
        self.Movement.move_left()
        self.Movement.get_back_to_first_position()

    # ==================================================================================================================
    # DEBUG
    def display_mouse(self):
        while True:
            print(pg.position(), end='\r')

    def test(self):
        self.test_ocr()
        # self.Fight.fight()
        return

    @staticmethod
    def test_ocr():
        img = pg.screenshot(region=Positions.RESSOURCE_REG)
        img = Images.change_color(img, min_value=140)
        value = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

        print(value)
        img.show()

    def take_screeshot(self):
        img = pg.screenshot()
        dir = 'images/fight/'
        n_images = len(os.listdir(dir))
        img.save(dir + f'houblon_{n_images}.png')
        time.sleep(1)


