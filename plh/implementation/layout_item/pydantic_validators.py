from __future__ import annotations

from .layout_item_base import LayoutItemBase


def validate_list(
    v: list[str | LayoutItemBase],
) -> list[LayoutItemBase]:
    supported_objects = []

    from . import devices

    objects = devices

    if v is None:
        return supported_objects

    for item in v:
        if isinstance(item, LayoutItemBase):
            supported_objects.append(item)

        elif item not in objects:
            raise ValueError(
                item + " is not found in " + LayoutItemBase.__name__ + " objects.",
            )

        else:
            supported_objects.append(objects[item])

    return supported_objects


def validate_instance(
    v: str | LayoutItemBase,
) -> LayoutItemBase:
    if isinstance(v, LayoutItemBase):
        return v

    from . import devices

    objects = devices
    identifier = v

    if identifier not in objects:
        raise ValueError(
            identifier + " is not found in " + LayoutItemBase.__name__ + " objects.",
        )

    return objects[identifier]
