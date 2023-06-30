from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import Tip

from .....Tools.AbstractClasses import UniqueObjectABC


@dataclass
class PipetteTip(UniqueObjectABC):
    UniqueIdentifier: str | int = field(init=False)
    TipInstance: Tip.BaseTip.Tip
    TipSupportDropoffSequence: str
    TipSupportPickupSequence: str
    WasteSequence: str

    def __post_init__(self):
        self.UniqueIdentifier = self.TipInstance.UniqueIdentifier
