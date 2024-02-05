from __future__ import annotations

from .ee_tip_stack import EETipStack
from .hamilton_ee_custom_ftr import HamiltonEECustomFTR
from .hamilton_ee_ntr import HamiltonEENTR
from .hamilton_ee_tip_base import HamiltonEETipBase
from .hamilton_ftr import HamiltonFTR
from .hamilton_ntr import HamiltonNTR
from .tip_base import TipBase

if True:
    from . import exceptions


__all__ = [
    "TipBase",
    "HamiltonFTR",
    "HamiltonNTR",
    "HamiltonEETipBase",
    "HamiltonEECustomFTR",
    "HamiltonEENTR",
    "EETipStack",
    "exceptions",
]

identifier = str
devices: dict[identifier, TipBase] = {}
