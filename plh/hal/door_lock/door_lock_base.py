from __future__ import annotations

from abc import abstractmethod

from pydantic import dataclasses

from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True)
class DoorLockBase(HALDevice, Interface):
    """Allows to unlock all doors on a system."""

    @abstractmethod
    def unlock(self: DoorLockBase) -> None:
        """Unlocks all doors"""
        ...

    @abstractmethod
    def lock(self: DoorLockBase) -> None:
        """Locks all doors"""
        ...
