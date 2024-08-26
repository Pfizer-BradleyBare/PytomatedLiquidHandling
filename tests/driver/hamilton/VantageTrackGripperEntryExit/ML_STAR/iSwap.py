from loguru import logger

from plh.device.hamilton_venus.backend import VantageTrackGripperEntryExit
from plh.device.hamilton_venus.ML_STAR import iSwap


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("GetPlate")
    command = iSwap.GetPlateCarrier.Command(
        options=iSwap.GetPlateCarrier.Options(
            LabwareID="Plate_1",
            GripWidth=87,
            OpenWidth=91,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, iSwap.GetPlateCarrier.Response)

    logger.info("PlacePlate")
    command = iSwap.PlacePlateCarrier.Command(
        options=iSwap.PlacePlateCarrier.Options(
            LabwareID="Plate_1",
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, iSwap.PlacePlateCarrier.Response)


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
