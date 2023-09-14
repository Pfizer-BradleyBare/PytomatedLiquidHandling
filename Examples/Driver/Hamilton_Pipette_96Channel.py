import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Driver.Hamilton.Pipette import CORE96Head
from PytomatedLiquidHandling.Driver.Hamilton.Tip import FTR


Backend = MicrolabStarBackend(
    "Example Star",
    os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

CommandInstance = FTR.LoadTips.Command(
    CustomErrorHandling=False,
    Options=FTR.LoadTips.Options(TipSequence="seq_Tips_FTR_1000ul"),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, FTR.LoadTips.Response)
# Load the tips on the deck. This makes sure the tip sequence is setup correctly

CommandInstance = FTR.GetTipPositions.Command(
    CustomErrorHandling=False,
    Options=FTR.GetTipPositions.Options(
        TipSequence="seq_Tips_FTR_1000ul",
        NumPositions=96,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, FTR.GetTipPositions.Response)
TipPositions = ResponseInstance.GetTipPositions()
# Get the tip positions for our tip pickup

CommandInstance = CORE96Head.Pickup.Command(
    CustomErrorHandling=False,
    Options=CORE96Head.Pickup.Options(Sequence="seq_Tips_FTR_1000ul"),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CORE96Head.Pickup.Response)
# pickup some tips

CommandInstance = CORE96Head.Aspirate.Command(
    CustomErrorHandling=False,
    Options=CORE96Head.Aspirate.Options(
        Sequence="Carrier14_Pos3_96WellPCRPlate200uL_1mLChannel",
        LiquidClass="HighVolume_Water_DispenseSurface_Empty",
        Volume=25,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CORE96Head.Aspirate.Response)
# Aspirate some liquid

CommandInstance = CORE96Head.Dispense.Command(
    CustomErrorHandling=False,
    Options=CORE96Head.Dispense.Options(
        Sequence="Carrier14_Pos3_96WellPCRPlate200uL_1mLChannel",
        LiquidClass="HighVolume_Water_DispenseSurface_Empty",
        Volume=25,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CORE96Head.Dispense.Response)
# Dispense some liquid

CommandInstance = CORE96Head.Eject.Command(
    CustomErrorHandling=False,
    Options=CORE96Head.Eject.Options(Sequence="core96externalwaste_0001"),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CORE96Head.Eject.Response)
# Eject some tips
