from __future__ import annotations

from pydantic import dataclasses

from plh.driver.HAMILTON import TrackGripper
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit

from .door_lock_base import *
from .door_lock_base import DoorLockBase


@dataclasses.dataclass(kw_only=True)
class HamiltonTrackGripperDoor(DoorLockBase):
    """Door locks associated with Track Gripper."""

    backend: VantageTrackGripperEntryExit

    def initialize(self: HamiltonTrackGripperDoor) -> None:
        """No initialization required."""

    def deinitialize(self: HamiltonTrackGripperDoor) -> None:
        """No deinitialization required."""

    def unlock(self: HamiltonTrackGripperDoor) -> None:
        """Unlocks doors associated with Track Gripper."""
        command = TrackGripper.LockUnlockDoors.Command(
            backend_error_handling=True,
            options=TrackGripper.LockUnlockDoors.Options(
                LockState=TrackGripper.LockUnlockDoors.LockStateOptions.Unlocked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, TrackGripper.LockUnlockDoors.Response)

    def lock(self: HamiltonTrackGripperDoor) -> None:
        """Locks doors associated with Track Gripper."""
        command = TrackGripper.LockUnlockDoors.Command(
            backend_error_handling=True,
            options=TrackGripper.LockUnlockDoors.Options(
                LockState=TrackGripper.LockUnlockDoors.LockStateOptions.Locked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, TrackGripper.LockUnlockDoors.Response)
