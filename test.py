from PytomatedLiquidHandling.Driver.Hamilton.Backend import VantageBackend
from PytomatedLiquidHandling.Tools.Logger import Logger
import os

LoggerInstance = Logger("Name", 0, os.path.dirname(__file__))

v = VantageBackend("Test", LoggerInstance)

v.StartBackend()

print("DONE")


v.StopBackend()
