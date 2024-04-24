from __future__ import annotations

from .deck_location_base import DeckLocationBase


def validate_list(
    v: list[str | DeckLocationBase],
) -> list[DeckLocationBase]:
    supported_objects = []

    from . import devices

    objects = devices

    if v is None:
        return supported_objects

    for item in v:
        if isinstance(item, DeckLocationBase):
            supported_objects.append(item)

        elif item not in objects:
            raise ValueError(
                item + " is not found in " + DeckLocationBase.__name__ + " objects.",
            )

        else:
            supported_objects.append(objects[item])

    return supported_objects


def validate_instance(
    v: str | DeckLocationBase,
) -> DeckLocationBase:
    if isinstance(v, DeckLocationBase):
        return v

    from . import devices

    objects = devices
    identifier = v

    if identifier not in objects:
        raise ValueError(
            identifier + " is not found in " + DeckLocationBase.__name__ + " objects.",
        )

    return objects[identifier]
