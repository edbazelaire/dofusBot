import time

from src.utils.CurrentBot import CurrentBot


class Sleeper:
    sleep_ctrs = {}

    @staticmethod
    def sleep(n):
        """ call a sleep for the current bot. The sleep will be saved so the BotManager can perform ohter tasks while
        'sleeping' """
        Sleeper.sleep_ctrs[CurrentBot.id] = (int(time.time()), n)

    @staticmethod
    def check_remaining_time(bot_id: int = None) -> bool:
        if bot_id is None:
            bot_id = CurrentBot.id

        # time already exceeded
        if bot_id not in Sleeper.sleep_ctrs.keys():
            return True

        n_seconds_remaining = Sleeper.sleep_ctrs[bot_id][1] - (time.time() - Sleeper.sleep_ctrs[bot_id][0])
        return n_seconds_remaining <= 0

