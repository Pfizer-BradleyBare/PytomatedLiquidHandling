import logging
import os

from PytomatedLiquidHandling import Logger
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Driver.Hamilton.Transport import IPG

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
# create a logger to log all actions

Backend = MicrolabStarBackend("Example Star", LoggerInstance)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

CommandInstance = IPG.GetPlate.Command(
    CustomErrorHandling=False,
    OptionsInstance=IPG.GetPlate.Options(
        PlateSequence="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
        GripWidth=79,
        OpenWidth=83,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(CommandInstance, CommandInstance.Response)
# Grab the plate.

CommandInstance = IPG.PlacePlate.Command(
    CustomErrorHandling=False,
    OptionsInstance=IPG.PlacePlate.Options(
        PlateSequence="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(CommandInstance, CommandInstance.Response)
# Put it back

# Done!
