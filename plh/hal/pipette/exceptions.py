from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LiquidClassCategoryNotSupportedError(Exception):
    """HAL device does not support your Labware. This can be thrown for any LayoutItem inputs.

    Attributes
    ----------
    Categories: List of category names and associated volumes tuple[Name,Volume] that were not supported
    """

    Categories: list[str]
