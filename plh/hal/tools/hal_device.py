from __future__ import annotations

from typing import ClassVar, Self

from pydantic import dataclasses, field_validator


@dataclasses.dataclass(kw_only=True)
class HALDevice:
    """A high level device that is part of a fully functioning automation system.

    Example: An automation system is, at minimum, made up of a deck (with carriers and labware) and a pipette.
    This simplified system is assumed to be able to aspirate and dispense any liquid that is compatible with the pipette.
    A more complex system may add heaters, shakers, vacuums, etc. to increase the capability of the system. All devices
    that increase the capability of an automation system shall be described by this class.

    Attributes:
        Indentifier: A unique name per each device base class. Facilitates organization and easy retrieval of devices by name.
    """

    hal_devices: ClassVar[dict[str, type[Self]]] = {}

    identifier: str

    @field_validator("Identifier", mode="after")
    @classmethod
    def __validation_identifier(cls: type[HALDevice], v: str) -> str:
        if " " in v:
            msg = "Spaces are not allowed in Identifiers. Please replace with underscores (_)."
            raise ValueError(msg)
        return v

    def __eq__(self: HALDevice, __value: HALDevice) -> bool:
        return (type(self).__name__ + self.identifier) == (
            type(__value).__name__ + __value.identifier
        )

    def __hash__(self: HALDevice) -> int:
        return hash(type(self).__name__ + self.identifier)

    def __init_subclass__(cls: type[HALDevice]) -> None:
        cls.hal_devices[cls.__name__] = cls
