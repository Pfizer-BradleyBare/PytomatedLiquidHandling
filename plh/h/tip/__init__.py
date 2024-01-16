from __future__ import annotations

from .hamilton_ee_ftr import HamiltonEEFTR
from .hamilton_ee_ntr import HamiltonEENTR
from .hamilton_ftr import HamiltonFTR
from .hamilton_ntr import HamiltonNTR
from .tip_base import TipBase

__all__ = ["HamiltonEEFTR", "HamiltonEENTR", "HamiltonFTR", "HamiltonNTR", "TipBase"]

identifier = str
devices: dict[identifier, TipBase] = {}
