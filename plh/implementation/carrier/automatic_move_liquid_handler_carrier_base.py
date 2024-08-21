from __future__ import annotations

from abc import abstractmethod

from pydantic import dataclasses

from .manual_move_liquid_handler_carrier_base import *
from .manual_move_liquid_handler_carrier_base import ManualMoveLiquidHandlerCarrierBase


@dataclasses.dataclass(kw_only=True, eq=False)
class AutomaticMoveLiquidHandlerCarrierBase(ManualMoveLiquidHandlerCarrierBase):
    """A carrier which can be accessed and moved by an autoloading mechanism."""

    @abstractmethod
    def move_in(self: AutomaticMoveLiquidHandlerCarrierBase) -> None:
        """Move the carrier into the backend using the backend."""
        ...

    @abstractmethod
    def move_out(self: AutomaticMoveLiquidHandlerCarrierBase) -> None:
        """Move the carrier out of the backend using the backend."""
        ...
