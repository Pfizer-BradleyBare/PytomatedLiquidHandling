from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC
from .LiquidClass import LiquidClass, LiquidClassCategory
from .PipetteTip import PipetteTip


@dataclass
class PipetteABC(InterfaceABC, HALObject):
    SupportedPipetteTips: list[PipetteTip]
    SupportedLabwares: list[Labware.PipettableLabware]
    SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC]
    SupportedLiquidClassCategories: list[LiquidClassCategory]

    @dataclass(kw_only=True)
    class Options(OptionsABC):
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

    def OptionsSupported(
        self,
        ListedOptionsInstance: list[Options],
    ) -> bool:
        for OptionsInstance in ListedOptionsInstance:
            if OptionsInstance.CurrentSourceVolume < OptionsInstance.TransferVolume:
                raise Exception("Not enough liquid in source...")
            # Check Source has enough volume

            DestinationLabware = OptionsInstance.DestinationLayoutItemInstance.Labware
            if not isinstance(DestinationLabware, Labware.PipettableLabware):
                raise Exception("This should never happen")
            if (
                OptionsInstance.CurrentDestinationVolume
                + OptionsInstance.TransferVolume
                > DestinationLabware.Wells.MaxVolume
            ):
                raise Exception(
                    "Destination well cannot support this volume. Overflow will occur"
                )
            # Check destination has enough room for volume

            if (
                OptionsInstance.SourceLayoutItemInstance.Labware
                not in self.SupportedLabwares
            ):
                return False

            if (
                OptionsInstance.DestinationLayoutItemInstance.Labware
                not in self.SupportedLabwares
            ):
                return False
            # Labwares are supported

            if (
                OptionsInstance.SourceLayoutItemInstance.DeckLocation
                not in self.SupportedDeckLocations
            ):
                return False
            if (
                OptionsInstance.DestinationLayoutItemInstance.DeckLocation
                not in self.SupportedDeckLocations
            ):
                return False
            # Check Deck locations are supported

            # Check liquid class categories are supported

        return True

    @abstractmethod
    def Transfer(
        self,
        ListedOptionsInstance: list[Options],
    ):
        ...

    @abstractmethod
    def TransferTime(
        self,
        ListedOptionsInstance: list[Options],
    ):
        ...
