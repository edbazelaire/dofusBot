class ErrorHandler:
    MAP_POSITION_ERROR = 0
    is_error = False

    @staticmethod
    def reset():
        ErrorHandler.is_error = False
        ErrorHandler.MAP_POSITION_ERROR = 0

    @staticmethod
    def warning(msg):
        print('Warning : ' + msg)

    @staticmethod
    def error(msg):
        print('Warning : ' + msg)