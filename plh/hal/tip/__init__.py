from __future__ import annotations

from .ee_tip_stack import EETipStack
from .exceptions import TierOutOfTipsError
from .hamilton_ee_custom_ftr import HamiltonEECustomFTR
from .hamilton_ee_ntr import HamiltonEENTR
from .hamilton_ee_tip_base import HamiltonEETipBase
from .hamilton_ftr import HamiltonFTR
from .hamilton_ntr import HamiltonNTR
from .tip_base import TipBase

__all__ = [
    "TipBase",
    "HamiltonFTR",
    "HamiltonNTR",
    "HamiltonEETipBase",
    "HamiltonEECustomFTR",
    "HamiltonEENTR",
    "EETipStack",
    "TierOutOfTipsError",
]

identifier = str
devices: dict[identifier, TipBase] = {}
