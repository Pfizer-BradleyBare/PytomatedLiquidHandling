from PytomatedLiquidHandling import Logger, Driver
from PytomatedLiquidHandling.Driver.Pipette import SingleChannel
from PytomatedLiquidHandling.Driver.Tip import NTR, FTR
import logging
import os

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
DriverHandlerInstance = Driver.Handler(LoggerInstance)
# Creates the handler so we can communicate with the Hamilton
