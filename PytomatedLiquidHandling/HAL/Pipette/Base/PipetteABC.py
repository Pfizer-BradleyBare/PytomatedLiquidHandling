from abc import abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC
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

    def __post_init__(self):
        self.SupportedPipetteTips = sorted(
            self.SupportedPipetteTips, key=lambda x: x.TipInstance.MaxVolume
        )

    def IsDeckLocationSupported(
        self, DeckLocation: DeckLocation.Base.DeckLocationABC
    ) -> bool:
        return DeckLocation in self.SupportedDeckLocations

    def IsLabwareSupported(self, Labware: Labware.PipettableLabware) -> bool:
        return Labware in self.SupportedLabwares

    def IsLiquidClassCategorySupported(self, Category: str) -> bool:
        for PipetteTip in self.SupportedPipetteTips:
            if PipetteTip.IsLiquidClassCategorySupported(Category):
                return True

        return False

    def _GetTip(self, LiquidClassCategory: str, Volume: float) -> PipetteTip:
        PossiblePipetteTips = [
            PipetteTip
            for PipetteTip in self.SupportedPipetteTips
            if PipetteTip.IsLiquidClassCategorySupported(LiquidClassCategory)
        ]

        for PipetteTip in PossiblePipetteTips:
            if PipetteTip.TipInstance.MaxVolume >= Volume:
                return PipetteTip

        return PossiblePipetteTips[-1]

    @abstractmethod
    def Transfer(self, ListedOptions: list[TransferOptions]):
        ...

    @abstractmethod
    def TransferTime(self, ListedOptions: list[TransferOptions]):
        ...
