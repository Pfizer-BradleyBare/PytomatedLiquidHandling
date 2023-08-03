from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Orchastrator import Orchastrator


@dataclass
class Transport:
    OrchastratorInstance: Orchastrator
