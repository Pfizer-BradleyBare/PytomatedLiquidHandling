import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.ML_STAR import iSwap

Backend = MicrolabSTAR(
    Identifier="Example Star",
    DeckLayoutPath=os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

CommandInstance = iSwap.GetPlate.Command(
    UserErrorHandling=False,
    Options=iSwap.GetPlate.Options(
        LabwareID="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
        GripWidth=79,
        OpenWidth=83,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(CommandInstance, iSwap.GetPlate.Response)
# Grab the plate.

CommandInstance = iSwap.PlacePlate.Command(
    UserErrorHandling=False,
    Options=iSwap.PlacePlate.Options(
        LabwareID="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(CommandInstance, iSwap.PlacePlate.Response)
# Put it back

# Done!
