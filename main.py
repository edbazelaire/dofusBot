from src.Bot import Bot
from src.components.Fight import Fight
from src.enums.ressources import Ressources

import time
import pyautogui


if __name__ == '__main__':
    bot = Bot([Ressources.HOUBLON, Ressources.SEIGLE])
    bot.run()
    # bot.test()

    # fight = Fight()
    # while True:
    #     if fight.check_combat_started():
    #         fight.fight()
    #         break

    # Bot.test_ocr()

    # bot = Bot([Ressources.HOUBLON])
    # bot.display_mouse()


