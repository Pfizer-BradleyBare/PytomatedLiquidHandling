from ..Tools.Logger import Logger

__Logger: Logger


def RegisterLogger(LoggerInstance: Logger):
    global __Logger
    __Logger = LoggerInstance


def GetLogger() -> Logger:
    global __Logger

    try:
        return __Logger
    except:
        raise Exception("Logger not registered. Please correct")
