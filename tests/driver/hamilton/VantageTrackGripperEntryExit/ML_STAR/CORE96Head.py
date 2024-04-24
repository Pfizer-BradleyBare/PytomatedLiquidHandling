from loguru import logger

from plh.device.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.device.HAMILTON.ML_STAR import CORE96Head


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("Pickup")
    command = CORE96Head.Pickup.Command(
        options=CORE96Head.Pickup.Options(
            LabwareID="FTR_1",
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, CORE96Head.Pickup.Response)

    logger.info("Aspirate")
    command = CORE96Head.Aspirate.Command(
        options=CORE96Head.Aspirate.Options(
            LabwareID="Plate_1",
            LiquidClass="StandardVolume_Water_DispenseSurface_Empty",
            Volume=100,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, CORE96Head.Aspirate.Response)

    logger.info("Dispense")
    command = CORE96Head.Dispense.Command(
        options=CORE96Head.Dispense.Options(
            LabwareID="Plate_1",
            LiquidClass="StandardVolume_Water_DispenseSurface_Empty",
            Volume=100,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, CORE96Head.Dispense.Response)

    logger.info("Eject")
    command = CORE96Head.Eject.Command(
        options=CORE96Head.Eject.Options(
            LabwareID="CORE96_Waste",
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, CORE96Head.Eject.Response)


if __name__ == "__main__":
    logger.enable("plh")

    backend = VantageTrackGripperEntryExit(
        identifier="Example Star",
        simulation_on=True,
    )

    backend.start()
    # Creates the backend so we can communicate with the Hamilton

    main(backend)

    input("Press <Enter> to quit.")

    backend.stop()
