from __future__ import annotations

from pydantic import dataclasses

from plh.driver.HAMILTON import TrackGripper
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True)
class HamiltonTrackGripperDoor(HALDevice, Interface):
    """Allows to unlock all doors on a system."""

    backend: VantageTrackGripperEntryExit

    def initialize(self: HamiltonTrackGripperDoor) -> None:
        """No initialization required."""

    def deinitialize(self: HamiltonTrackGripperDoor) -> None:
        """No deinitialization required."""

    def unlock(self: HamiltonTrackGripperDoor) -> None:
        """Unlocks door associated with Track Gripper."""
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
        """Locks door associated with Track Gripper."""
        command = TrackGripper.LockUnlockDoors.Command(
            backend_error_handling=True,
            options=TrackGripper.LockUnlockDoors.Options(
                LockState=TrackGripper.LockUnlockDoors.LockStateOptions.Locked,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, TrackGripper.LockUnlockDoors.Response)
