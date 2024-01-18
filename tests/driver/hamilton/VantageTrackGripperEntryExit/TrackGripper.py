from loguru import logger

from plh.driver.HAMILTON import TrackGripper
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("LockUnlockDoors - Lock")
    command = TrackGripper.LockUnlockDoors.Command(
        options=TrackGripper.LockUnlockDoors.Options(
            LockState=TrackGripper.LockUnlockDoors.LockStateOptions.Locked,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, TrackGripper.LockUnlockDoors.Response)

    logger.info("LockUnlockDoors - Unlock")
    command = TrackGripper.LockUnlockDoors.Command(
        options=TrackGripper.LockUnlockDoors.Options(
            LockState=TrackGripper.LockUnlockDoors.LockStateOptions.Unlocked,
        ),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, TrackGripper.LockUnlockDoors.Response)

    logger.info("CountLabwareInStack")

    command = TrackGripper.MoveToHomePosition.Command(
        options=TrackGripper.MoveToHomePosition.Options(),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, TrackGripper.LockUnlockDoors.Response)

    logger.info("GripPlateFromTaughtPosition")

    command = TrackGripper.GripPlateFromTaughtPosition.Command(
        options=TrackGripper.GripPlateFromTaughtPosition.Options(
            OpenWidth=135,
            TaughtPathName="",
        ),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, TrackGripper.GripPlateFromTaughtPosition.Response)

    logger.info("PlacePlateToTaughtPosition")

    command = TrackGripper.PlacePlateToTaughtPosition.Command(
        options=TrackGripper.PlacePlateToTaughtPosition.Options(
            OpenWidth=10,
            TaughtPathName="",
        ),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, TrackGripper.PlacePlateToTaughtPosition.Response)


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
