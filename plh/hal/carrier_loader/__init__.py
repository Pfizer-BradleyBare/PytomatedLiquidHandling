from __future__ import annotations

from .carrier_loader_base import CarrierLoaderBase
from .hamilton_star_autoload import HamiltonStarAutoload
from .hamilton_vantage_autoload import HamiltonVantageAutoload

__all__ = [
    "CarrierLoaderBase",
    "HamiltonStarAutoload",
    "HamiltonVantageAutoload",
]

identifier = str
devices: dict[identifier, CarrierLoaderBase] = {}
