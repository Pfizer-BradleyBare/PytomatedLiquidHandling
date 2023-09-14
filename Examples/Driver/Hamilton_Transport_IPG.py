import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Driver.Hamilton.Transport import IPG

Backend = MicrolabStarBackend(
    "Example Star",
    os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

CommandInstance = IPG.GetPlate.Command(
    CustomErrorHandling=False,
    Options=IPG.GetPlate.Options(
        PlateSequence="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
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
        PlateSequence="Carrier14_Pos1_96WellPCRPlate1200uL_1mLChannel",
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Response = Backend.GetResponse(CommandInstance, IPG.PlacePlate.Response)
# Put it back

# Done!
