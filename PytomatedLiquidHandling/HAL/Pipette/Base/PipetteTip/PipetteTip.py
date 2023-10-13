from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import Tip

from .LiquidClass import LiquidClass


@dataclass
class PipetteTip:
    TipInstance: Tip.Base.TipABC
    TipSupportDropoffSequence: str
    TipSupportPickupSequence: str
    WasteSequence: str
    SupportedLiquidClassCategories: dict[str, str]

    def IsLiquidClassCategorySupported(self, Category: str) -> bool:
        return Category in self.SupportedLiquidClassCategories

    def IsVolumeSupported(self, Volume: float) -> bool:
        return Volume <= self.TipInstance.MaxVolume
