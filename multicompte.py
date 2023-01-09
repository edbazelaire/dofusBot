from data.JobRoutines import CharNames
from src.BotManager import BotManager
from src.components.Inventory import Inventory
from src.enum.positions import Positions

if __name__ == '__main__':
    # init positions from window size
    Positions(game_window_id=0)

    botManager = BotManager(
        teams=[
            [CharNames.RALPHERTIN, CharNames.INCE_ROLA, CharNames.INCE_ROLA, CharNames.ALIC_CLARIA],
        ]
    )

    botManager.run()
