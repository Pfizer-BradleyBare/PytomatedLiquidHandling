from loguru import logger

from plh.device.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.device.HAMILTON.ML_STAR import ML_STAR


def main(backend: VantageTrackGripperEntryExit) -> None:
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

    backend = VantageTrackGripperEntryExit(
        identifier="Example Star",
        simulation_on=True,
    )

    backend.start()
    # Creates the backend so we can communicate with the Hamilton

    main(backend)

    input("Press <Enter> to quit.")

    backend.stop()
