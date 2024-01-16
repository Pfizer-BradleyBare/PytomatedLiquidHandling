from __future__ import annotations

from .closeable_container_base import CloseableContainerBase, OpenCloseOptions
from .hamilton_fliptube_landscape import HamiltonFlipTubeLandscape

__all__ = ["CloseableContainerBase", "HamiltonFlipTubeLandscape", "OpenCloseOptions"]
identifier = str
devices: dict[identifier, CloseableContainerBase] = {}
