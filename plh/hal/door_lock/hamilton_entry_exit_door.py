from __future__ import annotations

from pydantic import dataclasses

from plh.driver.HAMILTON import EntryExit
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit

from .door_lock_base import *
from .door_lock_base import DoorLockBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonEntryExitDoor(DoorLockBase):
    """Door locks associated with Entry Exit."""

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
