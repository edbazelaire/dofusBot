from src.utils.CurrentBot import CurrentBot
from colorama import Fore, Back, Style


class Displayer:
    @staticmethod
    def print(msg):
        print(f'[{CurrentBot.instance.char_name}] {Displayer.get_bot_color(CurrentBot.instance.id)} {msg} {Fore.RESET}')

    @staticmethod
    def get_bot_color(bot_id:int):
        if bot_id == 0:
            return Fore.BLUE
        if bot_id == 1:
            return Fore.YELLOW
        if bot_id == 2:
            return Fore.GREEN
        if bot_id == 3:
            return Fore.RED