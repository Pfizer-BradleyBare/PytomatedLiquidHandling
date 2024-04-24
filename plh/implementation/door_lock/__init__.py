from __future__ import annotations

from .door_lock_base import DoorLockBase
from .hamilton_entry_exit_door import HamiltonEntryExitDoor
from .hamilton_front_cover import HamiltonFrontCover
from .hamilton_track_gripper_door import HamiltonTrackGripperDoor

__all__ = [
    "DoorLockBase",
    "HamiltonFrontCover",
    "HamiltonTrackGripperDoor",
    "HamiltonEntryExitDoor",
]

identifier = str
devices: dict[identifier, DoorLockBase] = {}
