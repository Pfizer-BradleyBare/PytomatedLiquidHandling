import os

from loguru import logger

from PytomatedLiquidHandling.Driver.Hamilton import HSLTipCountingLib
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.ML_STAR import CORE96Head


def Main():
    logger.info(f"Executing Main() from {__file__}")

    CommandInstance = CORE96Head.Pickup.Command(
        BackendErrorHandling=False,
        Options=CORE96Head.Pickup.Options(LabwareID="FTR_1"),
    )
    Backend.ExecuteCommand(CommandInstance)
    Backend.WaitForResponseBlocking(CommandInstance)
    ResponseInstance = Backend.GetResponse(CommandInstance, CORE96Head.Pickup.Response)
    # pickup some tips

    CommandInstance = CORE96Head.Aspirate.Command(
        BackendErrorHandling=False,
        Options=CORE96Head.Aspirate.Options(
            LabwareID="Plate_1",
            LiquidClass="StandardVolume_Water_DispenseSurface_Empty",
            Volume=25,
        ),
    )
    Backend.ExecuteCommand(CommandInstance)
    Backend.WaitForResponseBlocking(CommandInstance)
    ResponseInstance = Backend.GetResponse(
        CommandInstance, CORE96Head.Aspirate.Response
    )
    # Aspirate some liquid

    CommandInstance = CORE96Head.Dispense.Command(
        BackendErrorHandling=False,
        Options=CORE96Head.Dispense.Options(
            LabwareID="Plate_1",
            LiquidClass="StandardVolume_Water_DispenseSurface_Empty",
            Volume=25,
        ),
    )
    Backend.ExecuteCommand(CommandInstance)
    Backend.WaitForResponseBlocking(CommandInstance)
    ResponseInstance = Backend.GetResponse(
        CommandInstance, CORE96Head.Dispense.Response
    )
    # Dispense some liquid

    CommandInstance = CORE96Head.Eject.Command(
        BackendErrorHandling=False,
        Options=CORE96Head.Eject.Options(LabwareID="CORE96_Waste"),
    )
    Backend.ExecuteCommand(CommandInstance)
    Backend.WaitForResponseBlocking(CommandInstance)
    ResponseInstance = Backend.GetResponse(CommandInstance, CORE96Head.Eject.Response)
    # Eject some tips


if __name__ == "__main__":
    logger.enable("PytomatedLiquidHandling")

    Backend = MicrolabSTAR(
        Identifier="Example Star",
        SimulationOn=True,
        DeckLayoutPath=os.path.join(os.path.dirname(__file__), "SimulationLayout.lay"),
    )
    Backend.StartBackend()
    # Creates the Backend so we can communicate with the Hamilton

    Main()

    input("Press <Enter> to quit.")

    Backend.StopBackend()
