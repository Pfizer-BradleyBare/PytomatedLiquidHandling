from __future__ import annotations

from .carrier_location_base import CarrierLocationBase


def validate_list(
    v: list[str | CarrierLocationBase],
) -> list[CarrierLocationBase]:
    supported_objects = []

    from . import devices

    objects = devices

    if v is None:
        return supported_objects

    for item in v:
        if isinstance(item, CarrierLocationBase):
            supported_objects.append(item)

        elif item not in objects:
            raise ValueError(
                item + " is not found in " + CarrierLocationBase.__name__ + " objects.",
            )

        else:
            supported_objects.append(objects[item])

    return supported_objects


def validate_instance(
    v: str | CarrierLocationBase,
) -> CarrierLocationBase:
    if isinstance(v, CarrierLocationBase):
        return v

    from . import devices

    objects = devices
    identifier = v

    if identifier not in objects:
        raise ValueError(
            identifier
            + " is not found in "
            + CarrierLocationBase.__name__
            + " objects.",
        )

    return objects[identifier]
