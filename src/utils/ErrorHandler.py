from datetime import datetime as dt


class ErrorHandler:
    is_error = False

    # TIME RULES
    LOAD_MAP_TIME = 10
    TRAVEL_MAP_TIME = 10

    # ERROR TYPES :
    MAP_NOT_CHANGED_ERROR = 0
    MAP_POSITION_ERROR = 1

    # MAX ALLOWED ERRORS BEFORE RESET
    MAX_ERRORS = {
        MAP_NOT_CHANGED_ERROR: 3,
        MAP_POSITION_ERROR: 2
    }

    # ERROR COUNTERS
    ERROR_CTRS = {
        MAP_NOT_CHANGED_ERROR: 0,
        MAP_POSITION_ERROR: 0,
    }

    @staticmethod
    def reset():
        ErrorHandler.is_error = False
        for error_type in ErrorHandler.ERROR_CTRS.keys():
            ErrorHandler.ERROR_CTRS[error_type] = 0

    @staticmethod
    def add_error(msg, error_type=None):
        print(f'[{dt.now().strftime("%Hh%M")}] ' + msg)
        if error_type is None:
            return

        if error_type not in ErrorHandler.ERROR_CTRS.keys():
            print(f"CONFIG ERROR : error ({ErrorHandler.get_error_name(error_type)}) not in ERROR_CTRS")
            return

        if error_type not in ErrorHandler.MAX_ERRORS.keys():
            print(f"CONFIG ERROR : error ({ErrorHandler.get_error_name(error_type)}) not in MAX_ERRORS")
            return

        ErrorHandler.ERROR_CTRS[error_type] += 1

        max_error = ErrorHandler.MAX_ERRORS[error_type]
        error_ctr = ErrorHandler.ERROR_CTRS[error_type]
        if error_ctr >= max_error:
            print(f'Max number of errors ({max_error}) for {ErrorHandler.get_error_name(error_type)} is reached  -> RESET')
            ErrorHandler.is_error = True

    @staticmethod
    def warning(msg, error_type=None):
        ErrorHandler.add_error('Warning : ' + msg, error_type)

    @staticmethod
    def error(msg, error_type=None):
        ErrorHandler.add_error('Error : ' + msg, error_type)

    @staticmethod
    def fatal_error(msg, error_type=None):
        ErrorHandler.add_error('FATAL ERROR  : ' + msg, error_type)
        exit()

    @staticmethod
    def get_error_name(error_type: str):
        for name, val in vars(ErrorHandler).items():
            if not name.endswith('_ERROR'):
                continue

            if val == error_type:
                return name

        print(f"CONFIG ERROR : Unable to find error_type with value ({error_type})")