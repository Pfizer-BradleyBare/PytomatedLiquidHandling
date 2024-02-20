from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.driver.tools import BackendBase
from plh.hal import backend


@dataclasses.dataclass(kw_only=True, eq=False)
class Interface(ABC):
    """Allows devices to abstract away functionality.

    Example: There are many systems which utilize pipette devices.
    Devices that inherit from interface will expose a set of abstract functions to simplify interaction across all systems.
    """

    backend: Annotated[
        BackendBase,
        BeforeValidator(backend.validate_instance),
    ]
    """The backend that will be used to execute physical actions. NOTE: devices are backend specific."""

    @abstractmethod
    def initialize(self: Interface) -> None: ...

    @abstractmethod
    def deinitialize(self: Interface) -> None: ...
