from __future__ import annotations

from abc import abstractmethod

from pydantic import dataclasses

from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True, eq=False)
class DoorLockBase(HALDevice, Interface):
    """Allows to unlock doors on a system."""

    @abstractmethod
    def unlock(self: DoorLockBase) -> None:
        """Unlocks doors associated with this device."""
        ...

    @abstractmethod
    def lock(self: DoorLockBase) -> None:
        """Locks doors associated with this device."""
        ...
