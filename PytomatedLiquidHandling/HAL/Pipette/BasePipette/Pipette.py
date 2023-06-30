from abc import abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import DeckLocation, Labware

from ....Tools.AbstractClasses import UniqueObjectABC
from ...Tools.AbstractClasses import InterfaceABC
from .Interface import TransferOptions
from .LiquidClass import LiquidClass, LiquidClassCategoryTracker
from .PipetteTip import PipetteTip, PipetteTipTracker


@dataclass
class Pipette(InterfaceABC, UniqueObjectABC):
    SupportedTipTrackerInstance: PipetteTipTracker
    SupportedLabwareTrackerInstance: Labware.LabwareTracker
    SupportedDeckLocationTrackerInstance: DeckLocation.DeckLocationTracker
    SupportedLiquidClassCategoryTrackerInstance: LiquidClassCategoryTracker

    def GetTip(self, Volume: float) -> PipetteTip:
        for PipetteTipInstance in self.SupportedTipTrackerInstance.GetObjectsAsList():
            if PipetteTipInstance.TipInstance.MaxVolume >= Volume:
                return PipetteTipInstance

        raise Exception("This should never happen")

    def GetLiquidClass(self, LiquidClassCategory: str, Volume: float) -> LiquidClass:
        for (
            LiquidClassInstance
        ) in self.SupportedLiquidClassCategoryTrackerInstance.GetObjectByName(
            LiquidClassCategory
        ).GetObjectsAsList():
            if Volume <= LiquidClassInstance.MaxVolume:
                return LiquidClassInstance

        raise Exception(
            "Volume exceeds that supported by this liquid class category..."
        )

    def OptionsSupported(
        self,
        OptionsTrackerInstance: TransferOptions.OptionsTracker,
    ) -> bool:
        for OptionsInstance in OptionsTrackerInstance.GetObjectsAsList():
            if OptionsInstance.CurrentSourceVolume < OptionsInstance.TransferVolume:
                raise Exception("Not enough liquid in source...")
            # Check Source has enough volume

            DestinationLabware = (
                OptionsInstance.DestinationLayoutItemInstance.LabwareInstance
            )
            if not isinstance(DestinationLabware, Labware.PipettableLabware):
                raise Exception("This should never happen")
            if (
                OptionsInstance.CurrentDestinationVolume
                + OptionsInstance.TransferVolume
                > DestinationLabware.LabwareWells.MaxVolume
            ):
                raise Exception(
                    "Destination well cannot support this volume. Overflow will occur"
                )
            # Check destination has enough room for volume

            if not self.SupportedLabwareTrackerInstance.IsTracked(
                OptionsInstance.SourceLayoutItemInstance.LabwareInstance.UniqueIdentifier
            ):
                return False
            if not self.SupportedLabwareTrackerInstance.IsTracked(
                OptionsInstance.DestinationLayoutItemInstance.LabwareInstance.UniqueIdentifier
            ):
                return False
            # Labwares are supported

            if not self.SupportedDeckLocationTrackerInstance.IsTracked(
                OptionsInstance.SourceLayoutItemInstance.DeckLocationInstance.UniqueIdentifier
            ):
                return False
            if not self.SupportedDeckLocationTrackerInstance.IsTracked(
                OptionsInstance.DestinationLayoutItemInstance.DeckLocationInstance.UniqueIdentifier
            ):
                return False
            # Check Deck locations are supported

            if not self.SupportedLiquidClassCategoryTrackerInstance.IsTracked(
                OptionsInstance.SourceLiquidClassCategory
            ):
                return False
            if not self.SupportedLiquidClassCategoryTrackerInstance.IsTracked(
                OptionsInstance.DestinationLiquidClassCategory
            ):
                return False
            # Check liquid class categories are supported

        return True

    @abstractmethod
    def Transfer(
        self,
        TransferOptionsTrackerInstance: TransferOptions.OptionsTracker,
    ):
        ...
