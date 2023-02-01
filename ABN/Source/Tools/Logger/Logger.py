import datetime
import logging
import os
import sys


def GenerateLogFilePath(LogFileFolderPath: str) -> str:
    return os.path.join(
        LogFileFolderPath,
        os.path.join(
            LogFileFolderPath,
            str(datetime.datetime.now().strftime("%d%b%Y-%H%M%S")) + "Log.ansi",
        ),
    )


class Logger(logging.Logger):
    def __init__(self, LoggerName: str, LogLevel: int, LoggingFilePath: str):
        logging.Logger.__init__(self, LoggerName, LogLevel)

        os.makedirs(os.path.dirname(LoggingFilePath), exist_ok=True)
        # make directory if it does not exists

        DefaultFormat = "[%(asctime)s] %(levelname)s\n%(message)s\n(%(threadName)s).%(module)s.%(funcName)s:%(lineno)d) <%(pathname)s>"

        file_handler = logging.FileHandler(LoggingFilePath)
        file_handler.setLevel(LogLevel)
        file_handler.setFormatter(CustomFormatter(DefaultFormat))
        self.addHandler(file_handler)
        # This flushes logs to the file path

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(LogLevel)
        stdout_handler.setFormatter(CustomFormatter(DefaultFormat))
        self.addHandler(stdout_handler)
        # This flushes logs to stdout

        sys.stderr = STDERRLogger(self)

        self.debug("Debug Message")
        self.info("Info Message")
        self.warning("Warning Message")
        self.error("Error Message")
        self.critical("Critical Message")


class STDERRLogger(object):
    def __init__(self, LoggerInstance: Logger):
        self.Message = ""
        self.LoggerInstance = LoggerInstance

    def write(self, message):
        self.Message += message

    def flush(self):
        if self.Message != "":
            self.LoggerInstance.critical(self.Message)
        self.Message = ""


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    debug = "\x1b[38;5;255m"
    info = "\x1b[38;5;39m"
    warning = "\x1b[38;5;226m"
    error = "\x1b[38;5;208m"
    critical = "\x1b[31;5;196m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.debug + self.fmt + self.reset,
            logging.INFO: self.info + self.fmt + self.reset,
            logging.WARNING: self.warning + self.fmt + self.reset,
            logging.ERROR: self.error + self.fmt + self.reset,
            logging.CRITICAL: self.critical + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
