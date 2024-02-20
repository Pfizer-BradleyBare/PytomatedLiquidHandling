from __future__ import annotations

from .tip_base import TipBase


def validate_instance(v: str | TipBase) -> TipBase:
    if isinstance(v, TipBase):
        return v

    from . import devices

    objects = devices
    identifier = v

    if identifier not in objects:
        raise ValueError(
            identifier + " is not found in " + TipBase.__name__ + " objects.",
        )

    return objects[identifier]
