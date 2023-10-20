import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.Transport import IPG

Backend = MicrolabSTAR(
    Identifier="Example Star",
    DeckLayoutPath=os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

CommandInstance = IPG.GetPlate.Command(
    CustomErrorHandling=False,
    Options=IPG.GetPlate.Options(
        LabwareID="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
        GripWidth=79,
        OpenWidth=83,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(CommandInstance, IPG.GetPlate.Response)
# Grab the plate.

CommandInstance = IPG.PlacePlate.Command(
    CustomErrorHandling=False,
    Options=IPG.PlacePlate.Options(
        LabwareID="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(CommandInstance, IPG.PlacePlate.Response)
# Put it back

# Done!
