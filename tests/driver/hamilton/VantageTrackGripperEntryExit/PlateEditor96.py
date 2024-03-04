import pathlib

from loguru import logger

from plh.driver.HAMILTON import PlateEditor96
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("EditPlate96")
    command = PlateEditor96.EditPlate96.Command()
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(
            command,
            PlateEditor96.EditPlate96.Response,
        ).SelectedPositions,
    )


if __name__ == "__main__":
    logger.enable("plh")

    backend = VantageTrackGripperEntryExit(
        identifier="Example Star",
        simulation_on=True,
        deck_layout=pathlib.Path(__file__).parent / "SimulationLayout.lay",
    )

    backend.start()
    # Creates the backend so we can communicate with the Hamilton

    main(backend)

    input("Press <Enter> to quit.")

    backend.stop()
