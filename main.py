from src.Bot import Bot
from src.components.Inventory import Inventory
from src.enum.positions import Positions
from src.enum.regions import Regions
from src.enum.ressources import Ressources

from src.utils.utils_fct import display_mouse

import sys

if __name__ == '__main__':
    region_name = Regions.CHAMP_ASTRUB
    ressources = []
    game_window_id = 0

    for i in range(len(sys.argv)):
        if sys.argv[i] == '--id':
            game_window_id = int(sys.argv[i+1])

        elif sys.argv[i] == '-reg' or sys.argv[i] == '--region':
            region_name = sys.argv[i+1]

        elif sys.argv[i] == '-res' or sys.argv[i] == '--ressources':
            ressources.append(sys.argv[i+1])

    # init positions from window size
    Positions(game_window_id=game_window_id)

    bot = Bot(
        region_name=Regions.CHAMP_ASTRUB,
        ressources=[
            # Ressources.HOUBLON,
            Ressources.TREFLE_A_5_FEUILLES,
            Ressources.ORTIE,
            # Ressources.SAUGE,
        ],
        crafts=[
            Ressources.CARASAU
        ]

    )
    bot.run()

    # DEBUG (not working if run() is active)
    Bot.test_ocr_map()
    display_mouse()


