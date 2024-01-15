import os

from loguru import logger
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.ML_STAR import Channel1000uL


def Main():
    logger.info(f"Executing Main() from {__file__}")

    logger.info("Pickup")
    Command = Channel1000uL.Pickup.Command(BackendErrorHandling=True, Options=[])
    for i in range(1, 9):
        Command.Options.append(
            Channel1000uL.Pickup.Options(
                LabwareID="FTR_1",
                PositionID=str(i),
                ChannelNumber=i,
            ),
        )

    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    ResponseInstance = Backend.GetResponse(Command, Channel1000uL.Pickup.Response)
    # Pickup our tips.
    # We are using the Tip information returned from the system
    # The channel number dictates exactly which channel picks up which tip.
    # We set BackendErrorHandling as True so the Hamilton software will handle errors for us.

    logger.info("Aspirate")
    Command = Channel1000uL.Aspirate.Command(BackendErrorHandling=True, Options=[])
    for i in range(1, 9):
        Command.Options.append(
            Channel1000uL.Aspirate.Options(
                ChannelNumber=i,
                LabwareID="Plate_1",
                PositionID="A1",
                LiquidClass="StandardVolume_Water_DispenseSurface_Empty",
                Volume=25,
            ),
        )

    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    ResponseInstance = Backend.GetResponse(Command, Channel1000uL.Aspirate.Response)
    # Aspirate some liquid from the same labware and same well 8 times
    # NOTE that the liquid class must be correct for the given aspiration volume.
    # The channel number dictates exactly which channel aspirates.
    # We set BackendErrorHandling as True so the Hamilton software will handle errors for us.

    logger.info("Dispense")
    Command = Channel1000uL.Dispense.Command(BackendErrorHandling=True, Options=[])
    for i in range(1, 9):
        Command.Options.append(
            Channel1000uL.Dispense.Options(
                ChannelNumber=i,
                LabwareID="Plate_2",
                PositionID="A1",
                LiquidClass="StandardVolume_Water_DispenseSurface_Empty",
                Volume=25,
            ),
        )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    ResponseInstance = Backend.GetResponse(Command, Channel1000uL.Dispense.Response)
    # Dispense liquid into the same container for example purposes.
    # NOTE that the liquid class must be correct for the given dispense volume.
    # The channel number dictates exactly which channel dispenses.
    # We set BackendErrorHandling as True so the Hamilton software will handle errors for us.

    logger.info("Eject")
    Command = Channel1000uL.Eject.Command(BackendErrorHandling=True, Options=[])
    for i in range(1, 9):
        Command.Options.append(
            Channel1000uL.Eject.Options(
                LabwareID="Waste",
                ChannelNumber=i,
                PositionID=str(i),
            ),
        )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    ResponseInstance = Backend.GetResponse(Command, Channel1000uL.Eject.Response)
    # Eject tips to waste.
    # We set BackendErrorHandling as True so the Hamilton software will handle errors for us.

    logger.info("GetLastLiquidLevel")
    Command = Channel1000uL.GetLastLiquidLevel.Command()
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Response = Backend.GetResponse(Command, Channel1000uL.GetLastLiquidLevel.Response)

    logger.info("FW_AspDis TODO")
    # TODO


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
