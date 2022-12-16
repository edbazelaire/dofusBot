import pyautogui as pg
import time
import os
import pytesseract

from src.enum.positions import Positions
from src.enum.images import Images
from src.enum.locations import Locations
from src.components.Fight import Fight
from src.components.Movement import Movement
from src.utils.ErrorHandler import ErrorHandler
from src.utils.utils_fct import wait_click_on


class Bot:
    MAX_TIME_SCANNING = 60
    HARVEST_TIME = 1
    CONFIDENCE = 0.6
    MAX_ALLOWED_RESSOURCES = 2500

    def __init__(self, region: str, ressources: list):
        self.images = {}

        self.region = region
        self.ressources = ressources
        self.get_images(ressources)
        self.last_num_ressources_checked = 0

        self.clicked_pos = []

        self.Movement = Movement(region, ressources)
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
            time.sleep(1)
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
            if self.Movement.position == self.Movement.next_position:
                self.Movement.get_next_position()

            self.Movement.go_to_next_pos()

    def scan(self):
        print('Scanning....')
        print("")

        if self.Movement.position not in self.Movement.path:
            ErrorHandler.error('current scanning position not in requested scanned maps')
            ErrorHandler.is_error = True

        start = time.time()
        isAny = True
        found_one = False
        while isAny:
            isAny = self.check_all_ressources()
            if not isAny or time.time() - start > self.MAX_TIME_SCANNING:
                break
            found_one = True
            time.sleep(self.HARVEST_TIME)

        # if we do not find any ressource on the map and that the OCR location is not ok with the calculated location
        if not found_one and not self.Movement.check_location():
            ErrorHandler.error("Scanning on wrong location -> reset")
            ErrorHandler.is_error = True

    def check_all_ressources(self):
        for ressource_name, images in self.images.items():
            # check if this ressource belong to this position
            if self.Movement.position not in Locations.RESSOURCES_LOCATIONS[self.region][ressource_name]:
                continue

            # check that this is not a "fake" location (only here to help path finding)
            if ressource_name == "fake":
                continue

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

        wait_click_on('images/screenshots/yes_button.png')

        # wait that map is loaded
        time.sleep(5)

        wait_click_on('images/screenshots/phoenix_statue.png', offset_x=20)
        wait_click_on(Images.get_fight(Images.CANCEL_POPUP), offset_x=5, offset_y=5)

        # wait until reaching phoenix statue
        time.sleep(5)

        # TODO : check in inventary that is not ghost anymore

        self.Movement.go_to(Locations.TOP_CORNER_CITY_LOCATION)

    # ==================================================================================================================
    # CHECKS
    def check_pods(self):
        num_ressources = 0
        for region in Positions.RESSOURCES_REG:
            img = pg.screenshot(region=region)
            img.resize((400, 200))
            img = Images.change_color(img, min_value=140)
            value = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

            value = 0 if value == '' else int(value)
            num_ressources += value

        # security : check that calculated number of ressources is not impossible
        if self.last_num_ressources_checked != 0 \
                and num_ressources != 0 \
                and abs(num_ressources - self.last_num_ressources_checked) > 500:
            ErrorHandler.warning("OCR ressource bad ressource recognition : "
                                 + f"\n    - num ressources checked {num_ressources}"
                                 + f"\n    - last num ressources checked {self.last_num_ressources_checked}"
                                 )
            # return False

        self.last_num_ressources_checked = num_ressources
        if num_ressources >= self.MAX_ALLOWED_RESSOURCES:
            print(f"MAX PODS : {num_ressources}")
            return True
        return False

    def check_is_ghost(self) -> bool:
        start = time.time()
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
        wait_click_on(self.Movement.city.BANK_NPC_IMAGE)

        # click on "accept" to access your bank inventory
        wait_click_on(Images.get_bank(Images.BANK_DIALOG_ACCESS), offset_x=50, offset_y=10)
        time.sleep(1)

        # select ressources tab
        pg.click(*Positions.BANK_PLAYER_INVENTORY_REG)
        time.sleep(1)

        # unload ressources
        wait_click_on(Images.get_bank(Images.BANK_TRANSFER_BUTTON), offset_x=5, offset_y=5, confidence=0.99)
        time.sleep(1)

        # validate ressources unloading
        wait_click_on(Images.get_bank(Images.BANK_TRANSFER_VISIBLE_OBJ_BTN))
        time.sleep(1)

        # close bank
        pg.click(*Positions.CLOSE_BANK_BUTTON_POSITION)

    # ==================================================================================================================
    # FIGHT
    def on_death(self):
        # move once left (because death pos is in building)
        self.Movement.move_left()
        self.Movement.get_back_to_first_position()

    # ==================================================================================================================
    # DEBUG
    def test(self):
        self.test_ocr()
        # self.Fight.fight()
        return

    @staticmethod
    def test_ocr():
        img = pg.screenshot(region=Positions.RESSOURCE3_REG)
        img = img.resize((200, 100))
        img = Images.change_color(img, min_value=140)
        value = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789,-')

        print(value)
        img.show()

    def take_screeshot(self):
        img = pg.screenshot()
        dir = 'images/fight/'
        n_images = len(os.listdir(dir))
        img.save(dir + f'houblon_{n_images}.png')
        time.sleep(1)


