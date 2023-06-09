import logging
import os

from PytomatedLiquidHandling import Logger
from PytomatedLiquidHandling.Driver.UnchainedLabs import CloseTray, OpenTray
from PytomatedLiquidHandling.Driver.UnchainedLabs.Backend import StunnerBackend

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
# create a logger to log all actions

Backend = StunnerBackend("Example Stunner", LoggerInstance, "10.37.145.113", 6300)

Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

print(str(Backend.GetStatus()))


Backend.StopBackend()
# Done!
