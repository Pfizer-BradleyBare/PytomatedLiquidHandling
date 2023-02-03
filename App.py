import sys

sys.dont_write_bytecode = True

import os
from logging import DEBUG

from App.Handler import Handler
from PytomatedLiquidHandling.Tools.Logger import GenerateLogFilePath, Logger

if __name__ == "__main__":

    LoggerInstance = Logger(
        "",
        DEBUG,
        GenerateLogFilePath(os.path.join(os.path.dirname(__file__), "Logging")),
    )

    HandlerInstance = Handler()

    HandlerInstance.StartServer()
    HandlerInstance.WaitForKill()
