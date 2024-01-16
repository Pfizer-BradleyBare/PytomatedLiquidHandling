from __future__ import annotations

from pydantic import dataclasses, field_validator

from plh.driver.tools import BackendBase
from plh.hal import backend


@dataclasses.dataclass(kw_only=True)
class Interface:
    """Allows devices to abstract away functionality.

    Example: There are many systems which utilize pipette devices.
    Devices that inherit from interface will expose a set of abstract functions to simplify interaction across all systems.

    Attributes:
        Backend: The backend that will be used to execute physical actions. NOTE: devices are backend specific.
        BackendErrorHandling: Allows users to handle errors directly on the system or to return them to the HAL device. NOTE: some
        backends may not support error handling on the system.
    """

    backend: BackendBase
    backend_error_handling: bool

    @field_validator("Backend", mode="before")
    @classmethod
    def __validate_backend(cls: type[Interface], v: str | BackendBase) -> BackendBase:
        if isinstance(v, BackendBase):
            return v

        objects = backend.devices
        identifier = v

        if identifier not in objects:
            raise ValueError(
                identifier + " is not found in " + BackendBase.__name__ + " objects.",
            )

        return objects[identifier]

    def initialize(self: Interface) -> None:
        if self.backend.is_running is False:
            self.backend.start()

    def deinitialize(self: Interface) -> None:
        if self.backend.is_running is True:
            self.backend.stop()
