from dataclasses import dataclass

from .LiquidClass import LiquidClass


@dataclass
class LiquidClassCategory:
    Name: str
    LiquidClasses: list[LiquidClass]
