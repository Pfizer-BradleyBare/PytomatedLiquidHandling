from __future__ import annotations

import json
from typing import ClassVar, Self, cast

from pydantic import BaseModel, dataclasses, field_validator


@dataclasses.dataclass(kw_only=True)
class HALDevice:
    """A high level device that is part of a fully functioning automation system.

    Example: An automation system is, at minimum, made up of a deck (with carriers and labware) and a pipette.
    This simplified system is assumed to be able to aspirate and dispense any liquid that is compatible with the pipette.
    A more complex system may add heaters, shakers, vacuums, etc. to increase the capability of the system. All devices
    that increase the capability of an automation system shall be described by this class.

    Attributes
    ----------
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

    def simple_representation(self) -> str:
        model_load_json = json.loads(BaseModel.model_dump_json(cast(BaseModel, self)))

        def get_id(model_json: dict) -> None:
            for key in model_json:
                value = model_json[key]

                if isinstance(value, list):
                    for index, item in enumerate(value):
                        if isinstance(item, dict) and "identifier" in item:
                            value[index] = item["identifier"]

                if isinstance(value, dict):
                    if "identifier" in value:
                        model_json[key] = value["identifier"]
                    else:
                        get_id(value)

        get_id(model_load_json)

        return json.dumps(model_load_json, indent=4)
