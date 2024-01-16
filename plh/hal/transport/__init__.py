from __future__ import annotations

from .transport_base import TransportBase

__all__ = ["TransportBase"]

identifier = str
devices: dict[identifier, TransportBase] = {}
