from src.Bot import Bot
from src.enum.regions import Regions
from src.enum.ressources import Ressources

from src.utils.utils_fct import display_mouse

if __name__ == '__main__':
    bot = Bot(
        region_name=Regions.PLAINES_CANIA,
        ressources=[
            Ressources.MALT,
            Ressources.CHANVRE,
            # Ressources.SEIGLE,
        ]
    )
    bot.run()

    # DEBUG (not working if run() is active)
    Bot.read_num_ressources(True)
    # Bot.test_ocr_map()
    display_mouse()


