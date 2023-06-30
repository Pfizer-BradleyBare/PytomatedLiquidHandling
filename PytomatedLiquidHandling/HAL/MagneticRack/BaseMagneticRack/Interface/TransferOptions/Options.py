from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import Pipette


@dataclass(kw_only=True)
class Options(Pipette.TransferOptions.Options):
    SourceLiquidClassCategory: str = field(init=False, default="")
    DestinationLiquidClassCategory: str = field(init=False, default="")
