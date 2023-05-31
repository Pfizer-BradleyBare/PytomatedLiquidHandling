import logging
import os

from PytomatedLiquidHandling import Logger
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Driver.Hamilton.Pipette import PortraitCORE8Channel
from PytomatedLiquidHandling.Driver.Hamilton.Tip import NTR

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

CommandInstance = NTR.LoadTips.Command(
    CustomErrorHandling=False,
    OptionsInstance=NTR.LoadTips.Options(
        TipSequence="seq_Tips_NTR_50ul",
        RackWasteSequence="Tip50_NTR_Waste",
        GripperSequence="seq_COREGripTool",
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
GeneratedWasteSequence = ResponseInstance.GetGeneratedWasteSequence()
# Load the tips on the deck. This makes sure the tip sequence is setup correctly

CommandInstance = NTR.GetTipPositions.Command(
    CustomErrorHandling=False,
    OptionsInstance=NTR.GetTipPositions.Options(
        TipSequence="seq_Tips_NTR_50ul",
        GeneratedRackWasteSequence=GeneratedWasteSequence,
        GripperSequence="seq_COREGripTool",
        NumPositions=8,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
TipPositions = ResponseInstance.GetTipPositions()
# Get the tip positions for our tip pickup

OptionsTrackerInstance = PortraitCORE8Channel.Pickup.OptionsTracker()
for i, Position in enumerate(TipPositions):
    OptionsTrackerInstance.LoadSingle(
        PortraitCORE8Channel.Pickup.Options(
            Sequence="seq_Tips_NTR_50ul", ChannelNumber=i + 1, SequencePosition=Position
        )
    )
CommandInstance = PortraitCORE8Channel.Pickup.Command(
    CustomErrorHandling=False, OptionsTrackerInstance=OptionsTrackerInstance
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
# pickup some tips

OptionsTrackerInstance = PortraitCORE8Channel.Aspirate.OptionsTracker()
for i, Position in enumerate(TipPositions):
    OptionsTrackerInstance.LoadSingle(
        PortraitCORE8Channel.Aspirate.Options(
            ChannelNumber=i + 1,
            Sequence="F32",
            SequencePosition=i + 1,
            LiquidClass="Tip_50ul_Water_DispenseSurface_Empty",
            Volume=25,
        )
    )
CommandInstance = PortraitCORE8Channel.Aspirate.Command(
    CustomErrorHandling=False, OptionsTrackerInstance=OptionsTrackerInstance
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
# Aspirate some liquid

OptionsTrackerInstance = PortraitCORE8Channel.Dispense.OptionsTracker()
for i, Position in enumerate(TipPositions):
    OptionsTrackerInstance.LoadSingle(
        PortraitCORE8Channel.Dispense.Options(
            ChannelNumber=i + 1,
            Sequence="F32",
            SequencePosition=i + 1,
            LiquidClass="Tip_50ul_Water_DispenseSurface_Empty",
            Volume=25,
            Mode=3,
        )
    )
CommandInstance = PortraitCORE8Channel.Dispense.Command(
    CustomErrorHandling=False, OptionsTrackerInstance=OptionsTrackerInstance
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
# Dispense some liquid

OptionsTrackerInstance = PortraitCORE8Channel.Eject.OptionsTracker()
for i, Position in enumerate(TipPositions):
    OptionsTrackerInstance.LoadSingle(
        PortraitCORE8Channel.Eject.Options(
            Sequence="Waste08", ChannelNumber=i + 1, SequencePosition=i + 1
        )
    )
CommandInstance = PortraitCORE8Channel.Eject.Command(
    CustomErrorHandling=False, OptionsTrackerInstance=OptionsTrackerInstance
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
# Eject some tips
