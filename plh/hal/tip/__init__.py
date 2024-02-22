from __future__ import annotations

from .hamilton_ee_ftr_1000uL import HamiltonEEFTR1000uL
from .hamilton_ee_ntr import HamiltonEENTR
from .hamilton_ee_tip_base import EETipStack, HamiltonEETipBase
from .hamilton_ftr import HamiltonFTR
from .hamilton_ntr import HamiltonNTR
from .pydantic_validators import validate_instance
from .tip_base import TipBase

if True:
    from . import exceptions


__all__ = [
    "TipBase",
    "HamiltonFTR",
    "HamiltonNTR",
    "HamiltonEETipBase",
    "HamiltonEEFTR1000uL",
    "HamiltonEENTR",
    "EETipStack",
    "exceptions",
    "validate_instance",
]

identifier = str
devices: dict[identifier, TipBase] = {}
