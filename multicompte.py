from src.BotManager import BotManager
from src.enum.positions import Positions

if __name__ == '__main__':
    # init positions from window size
    Positions(game_window_id=0)

    botManager = BotManager(1)

    botManager.run()
