from loguru import logger
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.driver.HAMILTON.ML_STAR import Channel1000uL


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("Pickup")
    command = Channel1000uL.Pickup.Command(
        options=[
            Channel1000uL.Pickup.Options(
                ChannelNumber=1,
                LabwareID="FTR_1",
                PositionID="1",
            ),
        ],
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, Channel1000uL.Pickup.Response)

    logger.info("Aspirate")
    command = Channel1000uL.Aspirate.Command(
        options=[
            Channel1000uL.Aspirate.Options(
                ChannelNumber=1,
                LabwareID="Plate_1",
                PositionID="A1",
                LiquidClass="StandardVolume_Water_DispenseSurface_Empty",
                Volume=100,
            ),
        ],
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, Channel1000uL.Aspirate.Response)

    logger.info("Dispense")
    command = Channel1000uL.Dispense.Command(
        options=[
            Channel1000uL.Dispense.Options(
                ChannelNumber=1,
                LabwareID="Plate_1",
                PositionID="A1",
                LiquidClass="StandardVolume_Water_DispenseSurface_Empty",
                Volume=100,
            ),
        ],
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, Channel1000uL.Dispense.Response)

    logger.info("Eject")
    command = Channel1000uL.Eject.Command(
        options=[
            Channel1000uL.Eject.Options(
                ChannelNumber=1,
                LabwareID="Waste",
                PositionID="1",
            ),
        ],
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, Channel1000uL.Eject.Response)

    logger.info("GetLastLiquidLevel")
    command = Channel1000uL.GetLastLiquidLevel.Command()
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            Channel1000uL.GetLastLiquidLevel.Response,
        ).ChannelLiquidLevels,
    )


if __name__ == "__main__":
    logger.enable("PytomatedLiquidHandling")

    backend = VantageTrackGripperEntryExit(
        identifier="Example Star",
        simulation_on=True,
    )

    backend.start()
    # Creates the backend so we can communicate with the Hamilton

    main(backend)

    input("Press <Enter> to quit.")

    backend.stop()
