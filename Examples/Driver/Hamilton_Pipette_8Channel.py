import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import (
    HamiltonStateCommandABC,
    MicrolabStarBackend,
)
from PytomatedLiquidHandling.Driver.Hamilton.Pipette import PortraitCORE8Channel
from PytomatedLiquidHandling.Driver.Hamilton.Tip import HSLTipCountingLib

Backend = MicrolabStarBackend(
    "Example Star",
    os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

ListedOptions = HSLTipCountingLib.Edit.ListedOptions(
    TipCounter="T", DialogTitle="Edit 1000uL Tip Positions"
)
ListedOptions.append(HSLTipCountingLib.Edit.Options("HT_L_0005"))
ListedOptions.append(HSLTipCountingLib.Edit.Options("HT_L_0003"))
ListedOptions.append(HSLTipCountingLib.Edit.Options("HT_L_0001"))
ListedOptions.append(HSLTipCountingLib.Edit.Options("HT_L_0002"))
ListedOptions.append(HSLTipCountingLib.Edit.Options("HT_L_0004"))
CommandInstance = HSLTipCountingLib.Edit.Command(
    CustomErrorHandling=False,
    ListedOptions=ListedOptions,
)

Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)

AvailablePositions = Backend.GetResponse(
    CommandInstance, HSLTipCountingLib.Edit.Response
).GetAvailablePositions()

ListedOptions = HSLTipCountingLib.Write.ListedOptions(TipCounter="T")
for Pos in AvailablePositions[96:]:
    ListedOptions.append(
        HSLTipCountingLib.Write.Options(
            LabwareID=Pos["LabwareID"], PositionID=Pos["PositionID"]
        )
    )
CommandInstance = HSLTipCountingLib.Write.Command(
    CustomErrorHandling=False, ListedOptions=ListedOptions
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Backend.GetResponse(CommandInstance, HSLTipCountingLib.Write.Response)


Backend.StopBackend()

quit()

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

CommandInstance = NTR.DiscardCurrentLayer.Command(
    CustomErrorHandling=False,
    Options=NTR.DiscardCurrentLayer.Options(
        TipSequence="seq_Tips_NTR_50ul",
        GeneratedRackWasteSequence=GeneratedWasteSequence,
        GripperSequence="seq_COREGripTool",
        NumPositions=8,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(
    CommandInstance, NTR.DiscardCurrentLayer.Response
)
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
