import pathlib

from loguru import logger

from plh.driver.HAMILTON.backend import MicrolabSTAR
from plh.driver.HAMILTON.ML_STAR import iSwap


def main(backend: MicrolabSTAR) -> None:
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

    backend = MicrolabSTAR(
        identifier="Example Star",
        simulation_on=True,
        deck_layout=pathlib.Path(__file__).parent.parent / "SimulationLayout.lay",
    )

    backend.start()
    # Creates the backend so we can communicate with the Hamilton

    main(backend)

    input("Press <Enter> to quit.")

    backend.stop()
