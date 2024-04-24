from __future__ import annotations

from . import BackendBase


def validate_instance(v: str | BackendBase) -> BackendBase:
    if isinstance(v, BackendBase):
        return v

    from . import devices

    objects = devices
    identifier = v

    if identifier not in objects:
        raise ValueError(
            identifier + " is not found in " + BackendBase.__name__ + " objects.",
        )

    return objects[identifier]
