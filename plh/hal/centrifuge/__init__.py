from __future__ import annotations

from .centrifuge_base import CentrifugeBase

__all__ = ["CentrifugeBase"]
identifier = str
devices: dict[identifier, CentrifugeBase] = {}
