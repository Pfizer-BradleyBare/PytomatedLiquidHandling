from pydantic import dataclasses

from .manual_move_liquid_handler_carrier_base import *
from .manual_move_liquid_handler_carrier_base import ManualMoveLiquidHandlerCarrierBase


@dataclasses.dataclass(kw_only=True, eq=False)
class AutomaticMoveLiquidHandlerCarrierBase(ManualMoveLiquidHandlerCarrierBase):
    """A carrier which can be accessed and moved by an autoloading mechanism."""
