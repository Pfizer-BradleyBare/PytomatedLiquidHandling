import logging
import os

from PytomatedLiquidHandling import API, HAL, Logger

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
# create a logger to log all actions

HALInstance = HAL.HAL(os.path.join(os.path.dirname(__file__), "Config"), LoggerInstance)

quit()
# Load everything

BackendTrackerInstance.GetObjectByName("Hammy").StartBackend()

PlateTransporter = TransportDeviceTrackerInstance
# devices
SamplePlate = LayoutItemTrackerInstance.GetObjectByName("Plate1")
DigestionPlate = LayoutItemTrackerInstance.GetObjectByName("Plate2")

OptionsTrackerInstance = HAL.TransportDevice.TransportOptions.OptionsTracker()
OptionsTrackerInstance.LoadSingle(
    HAL.TransportDevice.TransportOptions.Options(
        SourceLayoutItem=SamplePlate, DestinationLayoutItem=DigestionPlate
    )
)
PlateTransporter.Transport(OptionsTrackerInstance)

BackendTrackerInstance.GetObjectByName("Hammy").StopBackend()
