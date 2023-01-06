import os
import pyautogui as pg
from PIL.Image import Image

from src.enum.images import Images
from src.enum.positions import Positions
from src.utils.CurrentBot import CurrentBot
from src.utils.Sleeper import Sleeper


class Scanner:
    HARVEST_TIME = 2

    def __init__(self, parent, ressources):
        self.parent = parent
        self.ressources = ressources
        self.images = self.get_ressources_images(ressources)
        self.clicked_pos = []

    def scan(self) -> bool:
        """ scan the map for ressources """
        print('Scanning')

        for ressource_name, images in self.images.items():
            # check if this ressource belong to this position
            if self.parent.Movement.location not in self.parent.Movement.region.RESSOURCES_LOCATIONS[ressource_name]:
                continue

            for image in images:
                if self.find_ressource(image):
                    Sleeper.sleep(self.HARVEST_TIME)
                    return False

        print("\n")
        self.clicked_pos = []
        return True

    def find_ressource(self, image: Image) -> bool:
        all_pos = list(pg.locateAllOnScreen(
            image,
            confidence=0.75,
            region=Positions.WINDOW_REG
        ))

        for pos in all_pos:
            if (pos[0], pos[1]) in self.clicked_pos:
                continue

            self.clicked_pos.append((pos[0], pos[1]))

            if Positions.X_MAX > pos[0] > Positions.X_MIN and Positions.Y_MAX > pos[1] > Positions.Y_MIN:
                x = min(pos[0] + pos.width / 2, Positions.X_MAX)
                y = min(pos[1] + pos.height / 2, Positions.Y_MAX)
                pg.click(x, y)
                return True

        return False

    # ==================================================================================================================
    # UTILS
    @staticmethod
    def get_ressources_images(ressources: list):
        """ get only images of requested ressources """
        dir = 'images/ressources'
        images = {}
        for ressource_name in ressources:
            images[ressource_name] = [Images.load(dir + '/' + filename) for filename in os.listdir(dir) if filename.startswith(ressource_name)]
        return images