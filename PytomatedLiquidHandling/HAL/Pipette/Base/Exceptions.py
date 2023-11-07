from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .PipetteABC import PipetteABC


@dataclass
class LiquidClassCategoryNotSupportedError(BaseException):
    """HAL device does not support your Labware. This can be thrown for any LayoutItem inputs.

    Attributes:
    Categories: List of category names and associated volumes tuple[Name,Volume] that were not supported
    """

    Categories: list[tuple[str, float]]
