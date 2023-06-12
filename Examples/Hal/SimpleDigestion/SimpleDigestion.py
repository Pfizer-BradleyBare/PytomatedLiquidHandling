import logging
import os

from PytomatedLiquidHandling import HAL, Logger

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
# create a logger to log all actions

HAL.Backend.BackendLoader.LoadYaml(
    LoggerInstance, os.path.join(os.path.dirname(__file__), "Config_Backend.yaml")
)
