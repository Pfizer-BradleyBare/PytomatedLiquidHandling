import pathlib

from loguru import logger

from plh.hamilton_venus.backend import MicrolabSTAR
from plh.hamilton_venus.ML_STAR import ML_STAR


def main(backend: MicrolabSTAR) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("LockUnlockFrontCover - Lock")
    command = ML_STAR.LockUnlockFrontCover.Command(
        options=ML_STAR.LockUnlockFrontCover.Options(
            LockState=ML_STAR.LockUnlockFrontCover.LockStateOptions.Locked,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, ML_STAR.LockUnlockFrontCover.Response)

    logger.info("LockUnlockFrontCover - Unlock")
    command = ML_STAR.LockUnlockFrontCover.Command(
        options=ML_STAR.LockUnlockFrontCover.Options(
            LockState=ML_STAR.LockUnlockFrontCover.LockStateOptions.Unlocked,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, ML_STAR.LockUnlockFrontCover.Response)


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
