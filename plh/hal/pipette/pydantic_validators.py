from __future__ import annotations

from .pipette_base import PipetteBase


def validate_instance(
    v: str | PipetteBase,
) -> PipetteBase:
    if isinstance(v, PipetteBase):
        return v

    from . import devices

    objects = devices
    identifier = v

    if identifier not in objects:
        raise ValueError(
            identifier + " is not found in " + PipetteBase.__name__ + " objects.",
        )

    return objects[identifier]
