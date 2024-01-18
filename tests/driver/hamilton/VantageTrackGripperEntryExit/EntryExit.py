from loguru import logger

from plh.driver.HAMILTON import EntryExit
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("LockUnlockDoors - Lock")
    command = EntryExit.LockUnlockDoors.Command(
        options=EntryExit.LockUnlockDoors.Options(
            LockState=EntryExit.LockUnlockDoors.LockStateOptions.Locked,
        ),
        backend_error_handling=False,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, EntryExit.LockUnlockDoors.Response)

    logger.info("LockUnlockDoors - Unlock")
    command = EntryExit.LockUnlockDoors.Command(
        options=EntryExit.LockUnlockDoors.Options(
            LockState=EntryExit.LockUnlockDoors.LockStateOptions.Unlocked,
        ),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, EntryExit.LockUnlockDoors.Response)

    logger.info("CountLabwareInStack")

    command = EntryExit.CountLabwareInStack.Command(
        options=EntryExit.CountLabwareInStack.Options(
            ModuleNumber=1,
            StackNumber=3,
            LabwareID="",
            IsNTRRack=True,
        ),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, EntryExit.CountLabwareInStack.Response)

    logger.info("MoveRandomShelfAccess")

    command = EntryExit.MoveRandomShelfAccess.Command(
        options=EntryExit.MoveRandomShelfAccess.Options(
            ModuleNumber=1,
            StackNumber=3,
            Position=EntryExit.MoveRandomShelfAccess.PositionOptions.Bottom,
        ),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, EntryExit.MoveRandomShelfAccess.Response)

    logger.info("MoveRandomShelfAccess")

    command = EntryExit.MoveToBeam.Command(
        options=EntryExit.MoveToBeam.Options(
            ModuleNumber=1,
            StackNumber=3,
            OffsetFromBeam=0,
        ),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, EntryExit.MoveToBeam.Response)


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
