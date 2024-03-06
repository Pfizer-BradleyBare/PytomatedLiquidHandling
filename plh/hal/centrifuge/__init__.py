from __future__ import annotations

from .centrifuge_base import CentrifugeBase
from .hamilton_hig4 import HamiltonHig4

__all__ = ["CentrifugeBase", "HamiltonHig4"]
identifier = str
devices: dict[identifier, CentrifugeBase] = {}
