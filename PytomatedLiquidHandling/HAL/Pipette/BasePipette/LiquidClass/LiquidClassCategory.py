from dataclasses import dataclass

from .LiquidClass import LiquidClass


@dataclass
class LiquidClassCategory:
    LiquidClasses: list[LiquidClass]
