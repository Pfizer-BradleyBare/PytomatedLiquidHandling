from enum import Enum

from ....Tools.AbstractClasses import UniqueObjectABC
from .Interface.TipInterface import TipInterface


class Tip(UniqueObjectABC, TipInterface):
    def __init__(
        self,
        UniqueIdentifier: str,
        CustomErrorHandling: bool,
        PickupSequence: str,
        MaxVolume: float,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        TipInterface.__init__(self, CustomErrorHandling)
        self.PickupSequence: str = PickupSequence
        self.MaxVolume: float = MaxVolume
