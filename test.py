import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Tools.Logger import Logger

LoggerInstance = Logger("Name", 0, os.path.dirname(__file__))

v = MicrolabStarBackend("Test", LoggerInstance)

v.StartBackend()

print("DONE")

import time

time.sleep(10)
