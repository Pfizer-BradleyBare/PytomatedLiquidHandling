from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import dataclasses, field_validator

from plh.driver.tools import BackendBase
from plh.hal import backend


@dataclasses.dataclass(kw_only=True)
class Interface(ABC):
    """Allows devices to abstract away functionality.

    Example: There are many systems which utilize pipette devices.
    Devices that inherit from interface will expose a set of abstract functions to simplify interaction across all systems.
    """

    backend: BackendBase
    """The backend that will be used to execute physical actions. NOTE: devices are backend specific."""

    @field_validator("backend", mode="before")
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

    @abstractmethod
    def initialize(self: Interface) -> None:
        ...

    @abstractmethod
    def deinitialize(self: Interface) -> None:
        ...
