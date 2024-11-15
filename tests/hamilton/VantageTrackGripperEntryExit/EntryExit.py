from loguru import logger

from plh.hamilton_venus import EntryExit
from plh.hamilton_venus.backend import VantageTrackGripperEntryExit


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
            StackNumber=4,
            LabwareID="Tips_NTR_50uL_EntryExit",
            IsNTRRack=True,
        ),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    logger.info(
        backend.acknowledge(command, EntryExit.CountLabwareInStack.Response).NumLabware,
    )

    logger.info("MoveRandomShelfAccess")

    command = EntryExit.MoveRandomShelfAccess.Command(
        options=EntryExit.MoveRandomShelfAccess.Options(
            ModuleNumber=1,
            StackNumber=4,
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
            StackNumber=4,
            OffsetFromBeam=0,
        ),
        backend_error_handling=True,
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, EntryExit.MoveToBeam.Response)


if __name__ == "__main__":
    logger.enable("plh")

    backend = VantageTrackGripperEntryExit(
        identifier="Example Star",
        simulation_on=False,
    )

    backend.start()
    # Creates the backend so we can communicate with the Hamilton

    main(backend)

    input("Press <Enter> to quit.")

    backend.stop()
