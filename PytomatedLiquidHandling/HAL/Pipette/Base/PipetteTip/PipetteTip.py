from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import Tip


@dataclass
class PipetteTip:
    TipInstance: Tip.Base.TipABC
    TipSupportDropoffSequence: str
    TipSupportPickupSequence: str
    WasteSequence: str
