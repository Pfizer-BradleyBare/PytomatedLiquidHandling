from __future__ import annotations

from pydantic import dataclasses

from plh.driver.HAMILTON import EntryExit
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True)
class HamiltonEntryExitDoor(HALDevice, Interface):
    """Allows to unlock all doors on a system."""

    backend: VantageTrackGripperEntryExit

    def initialize(self: HamiltonEntryExitDoor) -> None:
        """No initialization required."""

    def deinitialize(self: HamiltonEntryExitDoor) -> None:
        """No deinitialization required."""

    def unlock(self: HamiltonEntryExitDoor) -> None:
        """Unlocks door associated with Entry Exit."""
        command = EntryExit.LockUnlockDoors.Command(
            backend_error_handling=True,
            options=EntryExit.LockUnlockDoors.Options(
                LockState=EntryExit.LockUnlockDoors.LockStateOptions.Unlocked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, EntryExit.LockUnlockDoors.Response)

    def lock(self: HamiltonEntryExitDoor) -> None:
        """Locks door associated with Entry Exit."""
        command = EntryExit.LockUnlockDoors.Command(
            backend_error_handling=True,
            options=EntryExit.LockUnlockDoors.Options(
                LockState=EntryExit.LockUnlockDoors.LockStateOptions.Locked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, EntryExit.LockUnlockDoors.Response)
