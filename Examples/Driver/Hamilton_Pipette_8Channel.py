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
    Options=NTR.LoadTips.Options(
        TipSequence="seq_Tips_NTR_50ul",
        RackWasteSequence="Tip50_NTR_Waste",
        GripperSequence="seq_COREGripTool",
    ),
)

Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, NTR.LoadTips.Response)
GeneratedWasteSequence = ResponseInstance.GetGeneratedWasteSequence()
# Load the tips on the deck. This makes sure the tip sequence is setup correctly

CommandInstance = NTR.GetTipPositions.Command(
    CustomErrorHandling=False,
    Options=NTR.GetTipPositions.Options(
        TipSequence="seq_Tips_NTR_50ul",
        GeneratedRackWasteSequence=GeneratedWasteSequence,
        GripperSequence="seq_COREGripTool",
        NumPositions=8,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, NTR.GetTipPositions.Response)
TipPositions = ResponseInstance.GetTipPositions()
# Get the tip positions for our tip pickup

ListedOptions = list()
for i, Position in enumerate(TipPositions):
    ListedOptions.append(
        PortraitCORE8Channel.Pickup.Options(
            Sequence="seq_Tips_NTR_50ul", ChannelNumber=i + 1, SequencePosition=Position
        )
    )
CommandInstance = PortraitCORE8Channel.Pickup.Command(
    CustomErrorHandling=False, ListedOptions=ListedOptions
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(
    CommandInstance, PortraitCORE8Channel.Pickup.Response
)
# pickup some tips

ListedOptions = list()
for i, Position in enumerate(TipPositions):
    ListedOptions.append(
        PortraitCORE8Channel.Aspirate.Options(
            ChannelNumber=i + 1,
            Sequence="F32",
            SequencePosition=i + 1,
            LiquidClass="Tip_50ul_Water_DispenseSurface_Empty",
            Volume=25,
        )
    )
CommandInstance = PortraitCORE8Channel.Aspirate.Command(
    CustomErrorHandling=False, ListedOptions=ListedOptions
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(
    CommandInstance, PortraitCORE8Channel.Aspirate.Response
)
# Aspirate some liquid

ListedOptions = list()
for i, Position in enumerate(TipPositions):
    ListedOptions.append(
        PortraitCORE8Channel.Dispense.Options(
            ChannelNumber=i + 1,
            Sequence="F32",
            SequencePosition=i + 1,
            LiquidClass="Tip_50ul_Water_DispenseSurface_Empty",
            Volume=25,
        )
    )
CommandInstance = PortraitCORE8Channel.Dispense.Command(
    CustomErrorHandling=False, ListedOptions=ListedOptions
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(
    CommandInstance, PortraitCORE8Channel.Dispense.Response
)
# Dispense some liquid

ListedOptions = list()
for i, Position in enumerate(TipPositions):
    ListedOptions.append(
        PortraitCORE8Channel.Eject.Options(
            Sequence="Waste08", ChannelNumber=i + 1, SequencePosition=i + 1
        )
    )
CommandInstance = PortraitCORE8Channel.Eject.Command(
    CustomErrorHandling=False, ListedOptions=ListedOptions
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(
    CommandInstance, PortraitCORE8Channel.Eject.Response
)
# Eject some tips
