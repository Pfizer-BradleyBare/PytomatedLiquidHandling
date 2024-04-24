from __future__ import annotations

from pydantic import dataclasses

from plh.device.tools import *
from plh.implementation import layout_item
from plh.implementation.deck_location import *
from plh.implementation.labware import *


@dataclasses.dataclass(kw_only=True)
class AspirateOptions:
    """Options that can be used for ```transfer``` and ```transfer_time```."""

    layout_item: layout_item.LayoutItemBase
    """Layout item to aspirate from."""

    position: int | str
    """Position in the layout item.
    NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself then the HAL device will position tips accordingly."""

    current_volume: float
    """Present volume in the specified layout_item position."""

    mix_cycles: int = 0
    """Cycles to mix before aspiration. 0 if not needed."""

    liquid_class_category: str
    """Liquid class category for aspiration."""


@dataclasses.dataclass(kw_only=True)
class DispenseOptions:
    """Options that can be used for ```transfer``` and ```transfer_time```."""

    layout_item: layout_item.LayoutItemBase
    """Layout item to dispense in to."""

    position: int | str
    """Position in the layout item.
    NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself then the HAL device will position tips accordingly."""

    current_volume: float
    """Present volume in the specified layout_item position."""

    mix_cycles: int = 0
    """Cycles to mix after dispense. 0 if not needed."""

    liquid_class_category: str
    """Liquid class category for dispense."""

    transfer_volume: float
    """Volume to dispense."""
