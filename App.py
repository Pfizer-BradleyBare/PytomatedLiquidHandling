import sys

sys.dont_write_bytecode = True

from App.Handler import Handler
from PytomatedLiquidHandling.Tools.Logger import GenerateLogFilePath, Logger

if __name__ == "__main__":

    HandlerInstance = Handler()

    HandlerInstance.StartServer()
    HandlerInstance.WaitForKill()
