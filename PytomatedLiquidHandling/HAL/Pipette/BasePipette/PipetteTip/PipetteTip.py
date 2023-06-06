from .....Tools.AbstractClasses import UniqueObjectABC
from ....Tip.BaseTip import Tip
from dataclasses import dataclass, field


@dataclass
class PipetteTip(UniqueObjectABC):
    UniqueIdentifier: str | int = field(init=False)
    TipInstance: Tip
    TipSupportDropoffSequence: str
    TipSupportPickupSequence: str
    WasteSequence: str

    def __post_init__(self):
        self.UniqueIdentifier = self.TipInstance.GetUniqueIdentifier()
