import os

from PytomatedLiquidHandling.Driver.Hamilton import Visual_NTR_Library
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.ML_STAR import Channel1000uL

Backend = MicrolabSTAR(
    Identifier="Example Star",
    DeckLayoutPath=os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)

import loguru

loguru.logger.enable("PytomatedLiquidHandling")


Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton


Command = Visual_NTR_Library.Channels_TipCounter_Edit.Command(
    Options=Visual_NTR_Library.Channels_TipCounter_Edit.ListedOptions(
        TipCounter="Custom", DialogTitle="Edit 50uL Tip Positions"
    )
)

TipLabwareIDs = [
    "TIP_50ul_L_NE_stack_0001_0003",
    "TIP_50ul_L_NE_stack_0002_0002",
    "TIP_50ul_L_NE_stack_0001_0001",
    "TIP_50ul_L_NE_stack_0002_0004",
    "TIP_50ul_L_NE_stack_0001_0004",
    "TIP_50ul_L_NE_stack_0001_0002",
    "TIP_50ul_L_NE_stack_0002_0003",
    "TIP_50ul_L_NE_stack_0002_0001",
]

for ID in TipLabwareIDs:
    Command.Options.append(
        Visual_NTR_Library.Channels_TipCounter_Edit.Options(LabwareID=ID)
    )

Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
AvailablePositions = Backend.GetResponse(
    Command, Visual_NTR_Library.Channels_TipCounter_Edit.Response
).AvailablePositions
# Execute our tip rack edit step on the Hamilton.
# This will prompt the user to select which tips are present and which are not.
# This information will then be returned to us to use for pipetting.

TipPositions = AvailablePositions[:8]
AvailablePositions = AvailablePositions[8:]
# We want to do a single pipetting step with 8 tips.

Command = Channel1000uL.Pickup.Command(BackendErrorHandling=True, Options=list())
for i, Position in enumerate(TipPositions):
    Command.Options.append(
        Channel1000uL.Pickup.Options(
            LabwareID=Position["LabwareID"],
            PositionID=Position["PositionID"],
            ChannelNumber=i + 1,
        )
    )

Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
ResponseInstance = Backend.GetResponse(Command, Channel1000uL.Pickup.Response)
# Pickup our tips.
# We are using the Tip information returned from the system
# The channel number dictates exactly which channel picks up which tip.
# We set BackendErrorHandling as True so the Hamilton software will handle errors for us.


Command = Channel1000uL.Aspirate.Command(BackendErrorHandling=True, Options=list())
for i, Position in enumerate(TipPositions):
    Command.Options.append(
        Channel1000uL.Aspirate.Options(
            ChannelNumber=i + 1,
            LabwareID="SMP_CAR_32_FlipTubes_A02_0001",
            PositionID="32",
            LiquidClass="Tip_50ul_Water_DispenseSurface_Empty",
            Volume=25,
        )
    )

Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
ResponseInstance = Backend.GetResponse(Command, Channel1000uL.Aspirate.Response)
# Aspirate some liquid from the same labware and same well 8 times
# NOTE that the liquid class must be correct for the given aspiration volume.
# The channel number dictates exactly which channel aspirates.
# We set BackendErrorHandling as True so the Hamilton software will handle errors for us.

Command = Channel1000uL.Dispense.Command(BackendErrorHandling=True, Options=list())
for i, Position in enumerate(TipPositions):
    Command.Options.append(
        Channel1000uL.Dispense.Options(
            ChannelNumber=i + 1,
            LabwareID="SMP_CAR_32_FlipTubes_A02_0001",
            PositionID="32",
            LiquidClass="Tip_50ul_Water_DispenseSurface_Empty",
            Volume=25,
        )
    )
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
ResponseInstance = Backend.GetResponse(Command, Channel1000uL.Dispense.Response)
# Dispense liquid into the same container for example purposes.
# NOTE that the liquid class must be correct for the given dispense volume.
# The channel number dictates exactly which channel dispenses.
# We set BackendErrorHandling as True so the Hamilton software will handle errors for us.

Command = Channel1000uL.Eject.Command(BackendErrorHandling=True, Options=list())
for i, Position in enumerate(TipPositions):
    Command.Options.append(
        Channel1000uL.Eject.Options(
            LabwareID="Waste",
            ChannelNumber=i + 1,
            PositionID=str(i + 1),
        )
    )
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
ResponseInstance = Backend.GetResponse(Command, Channel1000uL.Eject.Response)
# Eject tips to waste.
# We set BackendErrorHandling as True so the Hamilton software will handle errors for us.

Command = Visual_NTR_Library.Channels_TipCounter_Write.Command(
    Options=Visual_NTR_Library.Channels_TipCounter_Write.ListedOptions(
        TipCounter="My custom tip counter"
    )
)
for Pos in AvailablePositions:
    Command.Options.append(
        Visual_NTR_Library.Channels_TipCounter_Write.Options(
            LabwareID=Pos["LabwareID"], PositionID=Pos["PositionID"]
        )
    )

Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Backend.GetResponse(Command, Visual_NTR_Library.Channels_TipCounter_Write.Response)
# Write our tip counter so during the next tip edit it is already correctly selected.
