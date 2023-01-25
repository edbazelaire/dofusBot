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
        duration=None,
        team_index=1,
        teams=[
            [CharNames.PASCA_VIVIE, CharNames.RALPHERTIN, CharNames.INCE_ROLA],
            [CharNames.INCE_ROLA, CharNames.ALIC_CLARIA, CharNames.Bilias],
            [CharNames.Alizyann, CharNames.Ditoxynag],
            # [CharNames.Cinifurya],
        ]
    )

    botManager.run()
