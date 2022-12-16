from enum import Enum

from ....Tools.AbstractClasses import ObjectABC
from ...Layout import LayoutItem


class TempLimits:
    def __init__(
        self,
        StableTempDelta: float,
        MinimumTemp: float,
        MaximumTemp: float,
    ):
        self.StableTempDelta: float = StableTempDelta
        self.MinimumTemp: float = MinimumTemp
        self.MaximumTemp: float = MaximumTemp
