from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, dataclasses

from plh.device.HAMILTON.backend import HamiltonBackendBase
from plh.implementation import backend

from ..liquid_handler_deck_base import LiquidHandlerDeckBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVenusDeckBase(LiquidHandlerDeckBase):
    """Deck for Hamilton devices. Can be extended as needed."""

    backend: Annotated[
        HamiltonBackendBase,
        BeforeValidator(backend.validate_instance),
    ]

    def initialize(self: HamiltonVenusDeckBase) -> None:
        return super().initialize()

    def deinitialize(self: HamiltonVenusDeckBase) -> None:
        return super().deinitialize()
