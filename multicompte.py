from data.JobRoutines import CharNames
from src.BotManager import BotManager
from src.enum.positions import Positions
import pyautogui

if __name__ == '__main__':
    pyautogui.FAILSAFE = False

    # init positions from window size
    Positions(game_window_id=0)

    botManager = BotManager()

    botManager.run()
