import datetime
import logging
import os
import sys


class STDERRLogger(object):
    def __init__(self, LoggerInstance: logging.Logger):
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
        if record.name == "STDERR":
            record.lineno = 0

        self.Buffer.append(self.format(record))
        self.Buffer.append("</data-set>")
        File = open(self.FileName, "w")
        File.write("\n".join(self.Buffer))
        File.close()
        self.Buffer.pop(-1)


RootLogger = logging.getLogger()

LoggingFolderPath = os.path.join(os.path.dirname(sys.argv[0]), "Logging")
ColoredFolderPath = os.path.join(LoggingFolderPath, "Colored")
XMLFolderPath = os.path.join(LoggingFolderPath, "XML")

os.makedirs(LoggingFolderPath, exist_ok=True)
os.makedirs(ColoredFolderPath, exist_ok=True)
os.makedirs(XMLFolderPath, exist_ok=True)
# make directory if it does not exists

FileDatePrefix = str(datetime.datetime.now().strftime("%d%b%Y-%H%M%S"))

XMLFilePath = os.path.join(XMLFolderPath, FileDatePrefix + ".xml")

XMLFormat = ",,,record;;;,,,Time;;;%(asctime)s,,,/Time;;;,,,Name;;;%(name)s,,,/Name;;;,,,Line;;;%(lineno)d,,,/Line;;;,,,Message;;;%(message)s,,,/Message;;;,,,/record;;;"
Handler = XMLHandler(XMLFilePath)
Handler.setLevel(logging.DEBUG)
Handler.setFormatter(XMLFormatter(XMLFormat))
RootLogger.addHandler(Handler)
# This flushes logs to the xml file path

ColoredFilePath = os.path.join(ColoredFolderPath, FileDatePrefix + ".ansi")

ColoredFormat = "%(asctime)s|%(name)s|Line:%(lineno)d\n%(message)s"
Handler = logging.FileHandler(ColoredFilePath)
Handler.setLevel(logging.DEBUG)
Handler.setFormatter(ColoredFormatter(ColoredFormat))
RootLogger.addHandler(Handler)
# This flushes logs to the colored file path

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(ColoredFormatter(ColoredFormat))
RootLogger.addHandler(stdout_handler)
# This flushes logs to stdout

sys.stderr = STDERRLogger(logging.getLogger("STDERR"))

RootLogger.level = logging.DEBUG

from . import API, HAL, Driver
