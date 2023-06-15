from .....Pipette import TransferOptions
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Options(TransferOptions.Options):
    SourceLiquidClassCategory: str = field(init=False, default="")
    DestinationLiquidClassCategory: str = field(init=False, default="")
