import sys

sys.dont_write_bytecode = True

import os
from logging import DEBUG

from PytomatedLiquidHandling.API.Handler import Handler
from PytomatedLiquidHandling.Tools.Logger import GenerateLogFilePath, Logger

if __name__ == "__main__":

    LoggerInstance = Logger(
        "",
        DEBUG,
        GenerateLogFilePath(os.path.join(os.path.dirname(__file__), "Logging")),
    )

    Handler(
        LoggerInstance,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\App\\Configuration\\HAL",
    ).StartServer()
