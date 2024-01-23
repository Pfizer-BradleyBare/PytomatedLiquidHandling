from __future__ import annotations

from .hamilton_portrait_core8 import HamiltonPortraitCORE8

if True:
    pass
# This MUST come first so the if statement ensures that it does not get reordered by a formatter

from .exceptions import LiquidClassCategoryNotSupportedError
from .hamilton_core96 import HamiltonCORE96
from .liquid_class import LiquidClass
from .pipette_base import PipetteBase, TransferOptions
from .pipette_tip import PipetteTip

__all__ = [
    "PipetteBase",
    "PipetteTip",
    "LiquidClass",
    "TransferOptions",
    "HamiltonPortraitCORE8",
    "HamiltonCORE96",
    "LiquidClassCategoryNotSupportedError",
]

identifier = str
devices: dict[identifier, PipetteBase] = {}
