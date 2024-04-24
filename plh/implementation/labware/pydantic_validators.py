from __future__ import annotations

from .labware_base import LabwareBase


def validate_list(
    v: list[str | LabwareBase],
) -> list[LabwareBase]:
    supported_objects = []

    from . import devices

    objects = devices

    if v is None:
        return supported_objects

    for item in v:
        if isinstance(item, LabwareBase):
            supported_objects.append(item)

        elif item not in objects:
            raise ValueError(
                item + " is not found in " + LabwareBase.__name__ + " objects.",
            )

        else:
            supported_objects.append(objects[item])

    return supported_objects


def validate_instance(
    v: str | LabwareBase,
) -> LabwareBase:
    if isinstance(v, LabwareBase):
        return v

    from . import devices

    objects = devices
    identifier = v

    if identifier not in objects:
        raise ValueError(
            identifier + " is not found in " + LabwareBase.__name__ + " objects.",
        )

    return objects[identifier]
