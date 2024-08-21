from __future__ import annotations

from .deck_base import DeckBase


def validate_instance(
    v: str | DeckBase,
) -> DeckBase:
    if isinstance(v, DeckBase):
        return v

    from . import devices

    objects = devices
    identifier = v

    if identifier not in objects:
        raise ValueError(
            identifier + " is not found in " + DeckBase.__name__ + " objects.",
        )

    return objects[identifier]
