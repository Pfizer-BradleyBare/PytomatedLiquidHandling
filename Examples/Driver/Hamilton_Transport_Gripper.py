import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.Transport import COREGripper

Backend = MicrolabSTAR(
    Identifier="Example Star",
    DeckLayoutPath=os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton
CommandInstance = COREGripper.GetPlate.Command(
    CustomErrorHandling=False,
    Options=COREGripper.GetPlate.Options(
        GripperLabwareID="COREGripTool_OnWaste_1000ul_0001",
        PlateLabwareID="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
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
    Options=COREGripper.PlacePlate.Options(
        LabwareID="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
        EjectTool=COREGripper.PlacePlate.Options.YesNoOptions.Yes,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(CommandInstance, COREGripper.PlacePlate.Response)
# Put it back

# Done!
