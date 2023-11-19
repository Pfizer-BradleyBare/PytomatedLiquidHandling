import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.Pipette import PortraitCORE8Channel
from PytomatedLiquidHandling.Driver.Hamilton.Tip import Visual_NTR_Library

Backend = MicrolabSTAR(
    Identifier="Example Star",
    DeckLayoutPath=os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

ListedOptions = Visual_NTR_Library.Channels_TipCounter_Edit.ListedOptions(
    TipCounter="N", DialogTitle="Edit 1000uL Tip Positions"
)
ListedOptions.append(
    Visual_NTR_Library.Channels_TipCounter_Edit.Options("TIP_50ul_L_NE_stack_0001_0003")
)
ListedOptions.append(
    Visual_NTR_Library.Channels_TipCounter_Edit.Options("TIP_50ul_L_NE_stack_0002_0002")
)
ListedOptions.append(
    Visual_NTR_Library.Channels_TipCounter_Edit.Options("TIP_50ul_L_NE_stack_0001_0001")
)
ListedOptions.append(
    Visual_NTR_Library.Channels_TipCounter_Edit.Options("TIP_50ul_L_NE_stack_0002_0004")
)
ListedOptions.append(
    Visual_NTR_Library.Channels_TipCounter_Edit.Options("TIP_50ul_L_NE_stack_0001_0004")
)
ListedOptions.append(
    Visual_NTR_Library.Channels_TipCounter_Edit.Options("TIP_50ul_L_NE_stack_0001_0002")
)
ListedOptions.append(
    Visual_NTR_Library.Channels_TipCounter_Edit.Options("TIP_50ul_L_NE_stack_0002_0003")
)
ListedOptions.append(
    Visual_NTR_Library.Channels_TipCounter_Edit.Options("TIP_50ul_L_NE_stack_0002_0001")
)
CommandInstance = Visual_NTR_Library.Channels_TipCounter_Edit.Command(
    CustomErrorHandling=False,
    Options=ListedOptions,
)

Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
AvailablePositions = Backend.GetResponse(
    CommandInstance, Visual_NTR_Library.Channels_TipCounter_Edit.Response
).AvailablePositions

TipPositions = AvailablePositions[:8]

ListedOptions = list()
for i, Position in enumerate(TipPositions):
    ListedOptions.append(
        PortraitCORE8Channel.Pickup.Options(
            LabwareID=Position["LabwareID"],
            PositionID=Position["PositionID"],
            ChannelNumber=i + 1,
        )
    )
CommandInstance = PortraitCORE8Channel.Pickup.Command(
    CustomErrorHandling=False, Options=ListedOptions
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
            LabwareID="SMP_CAR_32_FlipTubes_A02_0001",
            PositionID="32",
            LiquidClass="Tip_50ul_Water_DispenseSurface_Empty",
            Volume=25,
        )
    )

ListedOptions[7].PositionID = "32"

CommandInstance = PortraitCORE8Channel.Aspirate.Command(
    CustomErrorHandling=True, Options=ListedOptions
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
            LabwareID="SMP_CAR_32_FlipTubes_A02_0001",
            PositionID="32",
            LiquidClass="Tip_50ul_Water_DispenseSurface_Empty",
            Volume=25,
        )
    )
CommandInstance = PortraitCORE8Channel.Dispense.Command(
    CustomErrorHandling=False, Options=ListedOptions
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
            LabwareID="Waste",
            ChannelNumber=i + 1,
            PositionID=str(i + 1),
        )
    )
CommandInstance = PortraitCORE8Channel.Eject.Command(
    CustomErrorHandling=False, Options=ListedOptions
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(
    CommandInstance, PortraitCORE8Channel.Eject.Response
)
# Eject some tips


ListedOptions = Visual_NTR_Library.Channels_TipCounter_Write.ListedOptions(
    TipCounter="N"
)
for Pos in AvailablePositions[8:]:
    ListedOptions.append(
        Visual_NTR_Library.Channels_TipCounter_Write.Options(
            LabwareID=Pos["LabwareID"], PositionID=Pos["PositionID"]
        )
    )
CommandInstance = Visual_NTR_Library.Channels_TipCounter_Write.Command(
    CustomErrorHandling=False, Options=ListedOptions
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Backend.GetResponse(
    CommandInstance, Visual_NTR_Library.Channels_TipCounter_Write.Response
)
