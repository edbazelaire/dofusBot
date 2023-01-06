from src.BotManager import BotManager
from src.enum.positions import Positions
from src.enum.regions import Regions
from src.enum.ressources import Ressources


if __name__ == '__main__':
    # init positions from window size
    Positions(game_window_id=0)

    botManager = BotManager(
        region_name=Regions.CHAMP_ASTRUB,
        ressources=[
            [
                Ressources.ORGES,
                Ressources.HOUBLON
            ],

            [
                Ressources.FRENE
            ]
        ],
        crafts=[
            [
                Ressources.CARASAU
            ],
            []
        ]
    )

    botManager.run()


