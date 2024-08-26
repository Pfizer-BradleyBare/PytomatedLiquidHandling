from loguru import logger

from plh.device.hamilton_venus import TrackGripper
from plh.device.hamilton_venus.backend import VantageTrackGripperEntryExit


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

    logger.info("MoveToHomePosition")

    command = TrackGripper.MoveToHomePosition.Command(
        options=TrackGripper.MoveToHomePosition.Options(),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, TrackGripper.LockUnlockDoors.Response)

    logger.info("GripPlateFromTaughtPosition")

    command = TrackGripper.GripPlateTaught.Command(
        options=TrackGripper.GripPlateTaught.Options(
            OpenWidth=1,
            TaughtPathName="On Deck Transition Point",
        ),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, TrackGripper.GripPlateTaught.Response)

    logger.info("PlacePlateToTaughtPosition")

    command = TrackGripper.PlacePlateTaught.Command(
        options=TrackGripper.PlacePlateTaught.Options(
            OpenWidth=1,
            TaughtPathName="On Deck Transition Point",
        ),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, TrackGripper.PlacePlateTaught.Response)


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
