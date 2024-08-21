from __future__ import annotations

from pydantic import dataclasses

from .deck_base import *
from .deck_base import DeckBase


@dataclasses.dataclass(kw_only=True, eq=False)
class GenericLiquidHandlerDeck(DeckBase):
    """A liquid handler deck. Liquid handlers typically have tracks upon which carriers are placed."""

    num_tracks: int
    """Number of tracks usable by carriers."""
