import time


class ErrorHandler:
    LOAD_MAP_TIME = 10
    TRAVEL_MAP_TIME = 10

    MAP_POSITION_ERROR = 0
    MAP_POSITION_ERROR_MAX = 2
    is_error = False

    @staticmethod
    def reset():
        ErrorHandler.is_error = False
        ErrorHandler.MAP_POSITION_ERROR = 0

    @staticmethod
    def warning(msg):
        print(f'[{time.time()}] Warning : ' + msg)

    @staticmethod
    def error(msg):
        print(f'[{time.time()}] Error : ' + msg)

    @staticmethod
    def fatal_error(msg):
        print(f'[{time.time()}] FATAL ERROR : ' + msg)
        exit()