from __future__ import annotations

from .transport_base import TransportBase


def validate_instance(
    v: str | TransportBase,
) -> TransportBase:
    # There is a circular dependacy in Transport. This is ONLY because it makes configuration simpler.
    # Basically DeckLocation should not depend on Transport. So we hide the dependacy above and here.
    # This may be a code smell. Not sure.

    if isinstance(v, TransportBase):
        return v

    from . import devices

    objects = devices
    identifier = v

    if identifier not in objects:
        raise ValueError(
            identifier + " is not found in " + TransportBase.__name__ + " objects.",
        )

    return objects[identifier]
