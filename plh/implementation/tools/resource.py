from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Annotated, ClassVar, cast

from pydantic import BaseModel, dataclasses, field_validator
from pydantic.functional_validators import BeforeValidator

from plh.device.tools import BackendBase
from plh.implementation import backend


@dataclasses.dataclass(kw_only=True, eq=False)
class Resource(ABC):
    """A high level device that is part of a fully functioning automation system.

    Example: An automation system is, at minimum, made up of a deck (with carriers and labware) and a pipette.
    This simplified system is assumed to be able to aspirate and dispense any liquid that is compatible with the pipette.
    A more complex system may add heaters, shakers, vacuums, etc. to increase the capability of the system. All devices
    that increase the capability of an automation system shall be described by this class.

    Resources will expose a set of abstract functions to simplify interaction across all systems.
    """

    resource_subclasses: ClassVar[dict[str, type[Resource]]] = {}
    """All subclasses"""

    identifier: str
    """A unique name. Facilitates organization and easy retrieval of devices by name."""

    backend: Annotated[
        BackendBase,
        BeforeValidator(backend.validate_instance),
    ]
    """The backend that will be used to execute physical actions. NOTE: devices are backend specific."""

    @field_validator("Identifier", mode="after")
    @classmethod
    def __validation_identifier(cls: type[Resource], v: str) -> str:
        if " " in v:
            msg = "Spaces are not allowed in Identifiers. Please replace with underscores (_)."
            raise ValueError(msg)
        return v

    def __eq__(self: Resource, __value: Resource) -> bool:
        return (type(self).__name__ + self.identifier) == (
            type(__value).__name__ + __value.identifier
        )

    def __hash__(self: Resource) -> int:
        return hash(type(self).__name__ + self.identifier)

    def __str__(self) -> str:
        return self.identifier

    def __init_subclass__(cls: type[Resource]) -> None:
        cls.resource_subclasses[cls.__name__] = cls

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

    @abstractmethod
    def initialize(self: Resource) -> None: ...

    @abstractmethod
    def deinitialize(self: Resource) -> None: ...
