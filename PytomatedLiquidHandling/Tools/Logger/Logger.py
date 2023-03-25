import datetime
import logging
import os
import sys


class Logger(logging.Logger):
    def __init__(self, LoggerName: str, LogLevel: int, LoggingFolderPath: str):
        logging.Logger.__init__(self, LoggerName, LogLevel)

        os.makedirs(LoggingFolderPath, exist_ok=True)
        os.makedirs(os.path.join(LoggingFolderPath, "Colored"), exist_ok=True)
        os.makedirs(os.path.join(LoggingFolderPath, "XML"), exist_ok=True)
        # make directory if it does not exists

        XMLFormat = ",,,record;;;,,,Time;;;%(asctime)s,,,/Time;;;,,,Level;;;%(levelname)s,,,/Level;;;,,,Message;;;%(message)s,,,/Message;;;,,,Thread;;;%(threadName)s,,,/Thread;;;,,,Module;;;%(module)s,,,/Module;;;,,,Function;;;%(funcName)s,,,/Function;;;,,,Line;;;%(lineno)d,,,/Line;;;,,,Path;;;%(pathname)s,,,/Path;;;,,,/record;;;"
        XMLPath = os.path.join(
            LoggingFolderPath,
            "XML",
            str(datetime.datetime.now().strftime("%d%b%Y-%H%M%S")) + "Log.xml",
        )
        file_handler = XMLHandler(XMLPath)
        file_handler.setLevel(LogLevel)
        file_handler.setFormatter(XMLFormatter(XMLFormat))
        self.addHandler(file_handler)
        # This flushes logs to the xml file path

        ColoredFormat = "[%(asctime)s] %(levelname)s\n%(message)s\n(%(threadName)s).%(module)s.%(funcName)s:%(lineno)d) <%(pathname)s>"
        ColoredPath = os.path.join(
            LoggingFolderPath,
            "Colored",
            str(datetime.datetime.now().strftime("%d%b%Y-%H%M%S")) + "Log.ansi",
        )
        file_handler = logging.FileHandler(ColoredPath)
        file_handler.setLevel(LogLevel)
        file_handler.setFormatter(ColoredFormatter(ColoredFormat))
        self.addHandler(file_handler)
        # This flushes logs to the colored file path

        file_handler.emit

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(LogLevel)
        stdout_handler.setFormatter(ColoredFormatter(ColoredFormat))
        self.addHandler(stdout_handler)
        # This flushes logs to stdout

        sys.stderr = STDERRLogger(self)

        # self.debug("Debug Message")
        # self.info("Info Message")
        # self.warning("Warning Message")
        # self.error("Error Message")
        # self.critical("Critical Message")


class STDERRLogger(object):
    def __init__(self, LoggerInstance: Logger):
        self.LoggerInstance = LoggerInstance
        self.Buffer = list()

    def write(self, Message):
        if len(self.Buffer) == 0 and Message == "\n":
            return

        if Message.endswith("\n"):
            self.Buffer.append(Message.removesuffix("\n"))
            self.LoggerInstance.critical("".join(self.Buffer))
            self.Buffer = list()
        else:
            self.Buffer.append(Message)

    def flush(self):
        pass


class ColoredFormatter(logging.Formatter):
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


class XMLFormatter(logging.Formatter):
    def __init__(self, fmt):
        super().__init__(fmt)
        self.fmt = fmt

    def format(self, record):
        return (
            super()
            .format(record)
            .replace("<", "")
            .replace(">", "")
            .replace(",,,", "<")
            .replace(";;;", ">")
        )


class XMLHandler(logging.Handler):
    def __init__(self, FileName: str):
        logging.Handler.__init__(self)
        self.FileName: str = FileName
        self.Buffer = list()
        self.Buffer.append("<data-set>")

    def emit(self, record):
        self.Buffer.append(self.format(record))
        self.Buffer.append("</data-set>")
        File = open(self.FileName, "w")
        File.write("\n".join(self.Buffer))
        File.close()
        self.Buffer.pop(-1)
