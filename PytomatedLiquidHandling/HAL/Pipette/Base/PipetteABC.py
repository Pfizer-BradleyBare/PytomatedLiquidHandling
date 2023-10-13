from abc import abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC
from .LiquidClass import LiquidClass, LiquidClassCategory
from .PipetteTip import PipetteTip


@dataclass(kw_only=True)
class TransferOptions(OptionsABC):
    SourceLayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    SourcePosition: int  # This is the labware well position. Not raw sequence position
    CurrentSourceVolume: float
    SourceMixCycles: int
    SourceLiquidClassCategory: str
    DestinationLayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    DestinationPosition: int  # This is the labware well position. Not raw sequence position
    CurrentDestinationVolume: float
    DestinationMixCycles: int
    DestinationLiquidClassCategory: str
    TransferVolume: float


@dataclass
class PipetteABC(InterfaceABC, HALObject):
    SupportedPipetteTips: list[PipetteTip]
    SupportedLabwares: list[Labware.PipettableLabware]
    SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC]
    SupportedLiquidClassCategories: list[LiquidClassCategory]

    def GetTip(self, Volume: float) -> PipetteTip:
        for PipetteTipInstance in self.SupportedPipetteTips:
            if PipetteTipInstance.TipInstance.MaxVolume >= Volume:
                return PipetteTipInstance

        raise Exception("This should never happen")

    def GetLiquidClass(self, LiquidClassCategory: str, Volume: float) -> LiquidClass:
        for LiquidClassCategoryInstance in self.SupportedLiquidClassCategories:
            if LiquidClassCategory == LiquidClassCategoryInstance.Name:
                for LiquidClass in LiquidClassCategoryInstance.LiquidClasses:
                    if Volume <= LiquidClass.MaxVolume:
                        return LiquidClass

                raise Exception(
                    "Volume exceeds that supported by this liquid class category..."
                )

        raise Exception("Liquid Class Category not found")

    @abstractmethod
    def Transfer(self, ListedOptions: list[TransferOptions]):
        ...

    @abstractmethod
    def TransferTime(self, ListedOptions: list[TransferOptions]):
        ...
