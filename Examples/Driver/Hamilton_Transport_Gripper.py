import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.ML_STAR import Channel1000uLCOREGrip

Backend = MicrolabSTAR(
    Identifier="Example Star",
    DeckLayoutPath=os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton
CommandInstance = Channel1000uLCOREGrip.GetPlate.Command(
    CustomErrorHandling=False,
    Options=Channel1000uLCOREGrip.GetPlate.Options(
        GripperLabwareID="COREGripTool_OnWaste_1000ul_0001",
        PlateLabwareID="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
        GripWidth=79,
        OpenWidth=83,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(CommandInstance, Channel1000uLCOREGrip.GetPlate.Response)
# Grab the plate.

CommandInstance = Channel1000uLCOREGrip.PlacePlate.Command(
    CustomErrorHandling=False,
    Options=Channel1000uLCOREGrip.PlacePlate.Options(
        LabwareID="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
        EjectTool=Channel1000uLCOREGrip.PlacePlate.Options.YesNoOptions.Yes,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(
    CommandInstance, Channel1000uLCOREGrip.PlacePlate.Response
)
# Put it back

# Done!
