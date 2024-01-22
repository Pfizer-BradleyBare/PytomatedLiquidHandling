from __future__ import annotations

from .ee_tip_stack import EETipStack
from .hamilton_ee_ftr import HamiltonEEFTR
from .hamilton_ee_ntr import HamiltonEENTR
from .hamilton_ftr import HamiltonFTR
from .hamilton_ntr import HamiltonNTR
from .tip_base import TipBase

__all__ = [
    "TipBase",
    "HamiltonFTR",
    "HamiltonNTR",
    "HamiltonEEFTR",
    "HamiltonEENTR",
    "EETipStack",
]

identifier = str
devices: dict[identifier, TipBase] = {}
