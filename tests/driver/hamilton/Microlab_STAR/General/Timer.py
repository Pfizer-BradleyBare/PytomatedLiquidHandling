import pathlib

from loguru import logger

from plh.device.hamilton_venus.backend import MicrolabSTAR
from plh.device.hamilton_venus.General import Timer


def main(backend: MicrolabSTAR) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("Start Timer")
    command = Timer.StartTimer.Command(
        options=Timer.StartTimer.Options(
            WaitTime=600,
            ShowTimer=True,
            IsStoppable=True,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, Timer.StartTimer.Response)


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
