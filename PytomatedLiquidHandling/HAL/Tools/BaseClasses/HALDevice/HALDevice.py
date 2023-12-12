from typing import ClassVar, Self, Type

from pydantic import dataclasses


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

    HALDevices: ClassVar[dict[str, Type[Self]]] = dict()

    Identifier: str

    def __eq__(self, __value: Type[Self]) -> bool:
        return (type(self).__name__ + self.Identifier) == (
            type(__value).__name__ + __value.Identifier
        )

    def __hash__(self) -> int:
        return hash(type(self).__name__ + self.Identifier)

    def __init_subclass__(cls):
        cls.HALDevices[cls.__name__] = cls
