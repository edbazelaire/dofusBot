from data.JobRoutines import CharNames
from src.BotManager import BotManager
from src.enum.positions import Positions
import pyautogui
from colorama import init

if __name__ == '__main__':
    init()
    pyautogui.FAILSAFE = False

    # init positions from window size
    Positions()

    botManager = BotManager(
        n_max=None,
        duration=4*3600,
        team_index=1,
        teams=[
            [CharNames.PASCA_VIVIE, CharNames.RALPHERTIN],
            [CharNames.INCE_ROLA, CharNames.ALIC_CLARIA],
            [CharNames.Alizyann, CharNames.Bilias],
            [CharNames.Cinifurya, CharNames.Ditoxynag],
        ]
    )

    botManager.run()
