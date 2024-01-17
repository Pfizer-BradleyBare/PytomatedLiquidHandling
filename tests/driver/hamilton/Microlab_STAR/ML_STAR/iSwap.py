import pathlib

from loguru import logger

from plh.driver.HAMILTON.backend import MicrolabSTAR
from plh.driver.HAMILTON.ML_STAR import iSwap


def main(backend: MicrolabSTAR) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("GetPlate")
    command = iSwap.GetPlate.Command(
        options=iSwap.GetPlate.Options(
            LabwareID="Plate_1",
            GripWidth=87,
            OpenWidth=91,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, iSwap.GetPlate.Response)

    logger.info("PlacePlate")
    command = iSwap.PlacePlate.Command(
        options=iSwap.PlacePlate.Options(
            LabwareID="Plate_1",
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, iSwap.PlacePlate.Response)


if __name__ == "__main__":
    logger.enable("PytomatedLiquidHandling")

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
