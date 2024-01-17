from __future__ import annotations

from pydantic import dataclasses, field_validator, model_validator

from plh.hal import deck_location, labware
from plh.hal.tools import HALDevice


@dataclasses.dataclass(kw_only=True)
class LayoutItemBase(HALDevice):
    identifier: str = "None"

    labware_id: str
    deck_location: deck_location.DeckLocationBase
    labware: labware.LabwareBase

    @field_validator("deck_location", mode="before")
    @classmethod
    def __deck_location_validate(
        cls: type[LayoutItemBase],
        v: str | deck_location.DeckLocationBase,
    ) -> deck_location.DeckLocationBase:
        if isinstance(v, deck_location.DeckLocationBase):
            return v

        objects = deck_location.devices
        identifier = v

        if identifier not in objects:
            raise ValueError(
                identifier
                + " is not found in "
                + deck_location.DeckLocationBase.__name__
                + " objects.",
            )

        return objects[identifier]

    @field_validator("labware", mode="before")
    @classmethod
    def __labware_validate(
        cls: type[LayoutItemBase],
        v: str | labware.LabwareBase,
    ) -> labware.LabwareBase:
        if isinstance(v, labware.LabwareBase):
            return v

        objects = labware.devices
        identifier = v

        if identifier not in objects:
            raise ValueError(
                identifier
                + " is not found in "
                + labware.LabwareBase.__name__
                + " objects.",
            )

        return objects[identifier]

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: LayoutItemBase):
        if v.identifier == "None":
            v.identifier = f"{v.deck_location.identifier}_{v.labware.identifier!s}"
        return v
