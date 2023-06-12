import logging
import os

from PytomatedLiquidHandling import Logger
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Driver.Hamilton.Transport import COREGripper

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
# create a logger to log all actions

Backend = MicrolabStarBackend("Example Star", LoggerInstance)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

CommandInstance = COREGripper.GetPlate.Command(
    CustomErrorHandling=False,
    OptionsInstance=COREGripper.GetPlate.Options(
        GripperSequence="seq_COREGripTool",
        PlateSequence="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
        GripWidth=79,
        OpenWidth=83,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(CommandInstance, COREGripper.GetPlate.Response)
# Grab the plate.

CommandInstance = COREGripper.PlacePlate.Command(
    CustomErrorHandling=False,
    OptionsInstance=COREGripper.PlacePlate.Options(
        PlateSequence="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
        EjectTool=COREGripper.PlacePlate.Options.YesNoOptions.Yes,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(CommandInstance, COREGripper.PlacePlate.Response)
# Put it back

# Done!
