from .....Tools.AbstractClasses import UniqueObjectABC
from ....Tip.BaseTip import Tip


class PipetteTip(UniqueObjectABC):
    def __init__(
        self,
        TipInstance: Tip,
        TipSupportDropoffSequence: str,
        TipSupportPickupSequence: str,
        WasteSequence: str,
    ):
        UniqueObjectABC.__init__(self, self.TipInstance.GetUniqueIdentifier())
        self.TipInstance: Tip = TipInstance
        self.TipSupportDropoffSequence: str = TipSupportDropoffSequence
        self.TipSupportPickupSequence: str = TipSupportPickupSequence
        self.WasteSequence: str = WasteSequence
