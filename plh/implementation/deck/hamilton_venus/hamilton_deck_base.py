from __future__ import annotations

from pydantic import dataclasses

from ..liquid_handler_deck_base import *
from ..liquid_handler_deck_base import LiquidHandlerDeckBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonDeckBase(LiquidHandlerDeckBase):
    """Deck for Hamilton devices. Can be extended as needed."""
