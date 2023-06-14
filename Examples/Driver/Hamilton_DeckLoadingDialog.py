import logging
import os

from PytomatedLiquidHandling import Logger
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Driver.Hamilton.DeckLoadingDialog import Carrier5Position

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
# create a logger to log all actions

Backend = MicrolabStarBackend(
    "Example Star",
    LoggerInstance,
    os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

OptionsTrackerInstance = Carrier5Position.OptionsTracker(
    Carrier3DImage=Carrier5Position.OptionsTracker.Carrier3DImageOptions.FTR5Position3D,
    Carrier2DImage=Carrier5Position.OptionsTracker.Carrier2DImageOptions.FTR5Position2D,
)
OptionsTrackerInstance.LoadSingle(
    Carrier5Position.Options(
        CarrierPosition=1,
        LabwareImage=Carrier5Position.Options.LabwareImageOptions.Biorad200uL96WellPlate,
        LabwareSupportingText="Hello!",
        LabwareActionText="Unload",
    )
)
OptionsTrackerInstance.LoadSingle(
    Carrier5Position.Options(
        CarrierPosition=4,
        LabwareImage=Carrier5Position.Options.LabwareImageOptions.Biorad200uL96WellPlate,
        LabwareSupportingText="Hello!",
        LabwareActionText="Unload",
    )
)
CommandInstance = Carrier5Position.Command(
    CustomErrorHandling=False, OptionsTrackerInstance=OptionsTrackerInstance
)

Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)

# Show dialog
