import logging
import os

from PytomatedLiquidHandling import Logger
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Driver.Hamilton.Pipette import CORE96Head
from PytomatedLiquidHandling.Driver.Hamilton.Tip import FTR

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
# create a logger to log all actions

Backend = MicrolabStarBackend(
    "Example Star",
    LoggerInstance,
    os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

CommandInstance = FTR.LoadTips.Command(
    CustomErrorHandling=False,
    OptionsInstance=FTR.LoadTips.Options(TipSequence="seq_Tips_FTR_1000ul"),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
# Load the tips on the deck. This makes sure the tip sequence is setup correctly

CommandInstance = FTR.GetTipPositions.Command(
    CustomErrorHandling=False,
    OptionsInstance=FTR.GetTipPositions.Options(
        TipSequence="seq_Tips_FTR_1000ul",
        NumPositions=96,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
TipPositions = ResponseInstance.GetTipPositions()
# Get the tip positions for our tip pickup

CommandInstance = CORE96Head.Pickup.Command(
    CustomErrorHandling=False,
    OptionsInstance=CORE96Head.Pickup.Options(Sequence="seq_Tips_FTR_1000ul"),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
# pickup some tips

CommandInstance = CORE96Head.Aspirate.Command(
    CustomErrorHandling=False,
    OptionsInstance=CORE96Head.Aspirate.Options(
        Sequence="Carrier14_Pos3_96WellPCRPlate200uL_1mLChannel",
        LiquidClass="HighVolume_Water_DispenseSurface_Empty",
        Volume=25,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
# Aspirate some liquid

CommandInstance = CORE96Head.Dispense.Command(
    CustomErrorHandling=False,
    OptionsInstance=CORE96Head.Dispense.Options(
        Sequence="Carrier14_Pos3_96WellPCRPlate200uL_1mLChannel",
        LiquidClass="HighVolume_Water_DispenseSurface_Empty",
        Volume=25,
    ),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
# Dispense some liquid

CommandInstance = CORE96Head.Eject.Command(
    CustomErrorHandling=False,
    OptionsInstance=CORE96Head.Eject.Options(Sequence="core96externalwaste_0001"),
)
Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)
ResponseInstance = Backend.GetResponse(CommandInstance, CommandInstance.Response)
# Eject some tips
