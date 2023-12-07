import os

from PytomatedLiquidHandling.Driver.Hamilton import HSLTipCountingLib
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.ML_STAR import CORE96Head

Backend = MicrolabSTAR(
    Identifier="Example Star",
    DeckLayoutPath=os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

ListedOptions = HSLTipCountingLib.Edit.ListedOptions(
    TipCounter="N", DialogTitle="Edit 1000uL Tip Positions"
)
ListedOptions.append(HSLTipCountingLib.Edit.Options(LabwareID="HT_L_0001"))
ListedOptions.append(HSLTipCountingLib.Edit.Options(LabwareID="HT_L_0002"))
ListedOptions.append(HSLTipCountingLib.Edit.Options(LabwareID="HT_L_0003"))
ListedOptions.append(HSLTipCountingLib.Edit.Options(LabwareID="HT_L_0004"))
ListedOptions.append(HSLTipCountingLib.Edit.Options(LabwareID="HT_L_0005"))
CommandInstance = HSLTipCountingLib.Edit.Command(
    Options=ListedOptions,
)

Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
AvailablePositions = Backend.GetResponse(
    CommandInstance, HSLTipCountingLib.Edit.Response
).AvailablePositions

CommandInstance = CORE96Head.Pickup.Command(
    BackendErrorHandling=False,
    Options=CORE96Head.Pickup.Options(LabwareID=AvailablePositions[0]["LabwareID"]),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CORE96Head.Pickup.Response)
# pickup some tips

CommandInstance = CORE96Head.Aspirate.Command(
    BackendErrorHandling=False,
    Options=CORE96Head.Aspirate.Options(
        LabwareID="Carrier14_Pos3_96WellPCRPlate200uL_1mLChannel",
        LiquidClass="HighVolume_Water_DispenseSurface_Empty",
        Volume=25,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CORE96Head.Aspirate.Response)
# Aspirate some liquid

CommandInstance = CORE96Head.Dispense.Command(
    BackendErrorHandling=False,
    Options=CORE96Head.Dispense.Options(
        LabwareID="Carrier14_Pos3_96WellPCRPlate200uL_1mLChannel",
        LiquidClass="HighVolume_Water_DispenseSurface_Empty",
        Volume=25,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CORE96Head.Dispense.Response)
# Dispense some liquid

CommandInstance = CORE96Head.Eject.Command(
    BackendErrorHandling=False,
    Options=CORE96Head.Eject.Options(LabwareID="core96externalwaste_0001"),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CORE96Head.Eject.Response)
# Eject some tips

ListedOptions = HSLTipCountingLib.Write.ListedOptions(TipCounter="N")
for Pos in AvailablePositions[96:]:
    ListedOptions.append(
        HSLTipCountingLib.Write.Options(
            LabwareID=Pos["LabwareID"], PositionID=Pos["PositionID"]
        )
    )
CommandInstance = HSLTipCountingLib.Write.Command(Options=ListedOptions)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
Backend.GetResponse(CommandInstance, HSLTipCountingLib.Write.Response)
