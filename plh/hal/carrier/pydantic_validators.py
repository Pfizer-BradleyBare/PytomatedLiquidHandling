from __future__ import annotations

from .carrier_base import CarrierBase


def validate_instance(
    v: str | CarrierBase,
) -> CarrierBase:
    if isinstance(v, CarrierBase):
        return v

    from . import devices

    objects = devices
    identifier = v

    if identifier not in objects:
        raise ValueError(
            identifier + " is not found in " + CarrierBase.__name__ + " objects.",
        )

    return objects[identifier]


def validate_list(
    v: list[str | CarrierBase],
) -> list[CarrierBase]:
    supported_objects = []

    from . import devices

    objects = devices

    if v is None:
        return supported_objects

    for item in v:
        if isinstance(item, CarrierBase):
            supported_objects.append(item)

        elif item not in objects:
            raise ValueError(
                item + " is not found in " + CarrierBase.__name__ + " objects.",
            )

        else:
            supported_objects.append(objects[item])

    return supported_objects
