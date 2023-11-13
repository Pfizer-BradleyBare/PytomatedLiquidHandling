from abc import abstractmethod
from dataclasses import dataclass
from math import ceil
from typing import Any

from pydantic import field_validator

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools import AbstractClasses

from .PipetteTip import PipetteTip


@dataclass(kw_only=True)
class TransferOptions(OptionsABC):
    SourceLayoutItemInstance: LayoutItem.CoverablePlate | LayoutItem.Plate
    SourcePosition: int | str
    # This is the labware well position. Numeric or alphanumeric.
    # NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself and the HAL device will position tips accordingly
    CurrentSourceVolme: float
    SourceMixCycles: int
    SourceLiquidClassCategory: str
    DestinationLayoutItemInstance: LayoutItem.CoverablePlate | LayoutItem.Plate
    DestinationPosition: int | str
    # This is the labware well position. Numeric or alphanumeric.
    # NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself and the HAL device will position tips accordingly
    CurrentDestinationVolume: float
    DestinationMixCycles: int
    DestinationLiquidClassCategory: str
    TransferVolume: float


class PipetteABC(AbstractClasses.Interface, AbstractClasses.HALDevice):
    SupportedTips: list[PipetteTip]
    SupportedSourceLabwares: list[Labware.PipettableLabware]
    SupportedDestinationLabwares: list[Labware.PipettableLabware]
    SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC]

    @field_validator("SupportedTips", mode="after")
    def __SupportedTipsValidate(cls, v):
        return sorted(v, key=lambda x: x.Tip.Volume)

    @field_validator("SupportedDeckLocations", mode="before")
    def __SupportedDeckLocationsValidate(cls, v):
        SupportedObjects = list()

        Objects = DeckLocation.Devices

        for Identifier in v:
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + DeckLocation.Base.DeckLocationABC.__name__
                    + " objects."
                )

            SupportedObjects.append(Objects[Identifier])

        return SupportedObjects

    @field_validator(
        "SupportedSourceLabwares", "SupportedDestinationLabwares", mode="before"
    )
    def __SupportedLabwaresValidate(cls, v):
        SupportedObjects = list()

        Objects = Labware.Devices

        for Identifier in v:
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + Labware.Base.LabwareABC.__name__
                    + " objects."
                )

            SupportedObjects.append(Objects[Identifier])

        return SupportedObjects

    def model_post_init(self, __context: Any) -> None:
        AbstractClasses.HALDevice.model_post_init(self, __context)
        AbstractClasses.Interface.model_post_init(self, __context)
        self.SupportedTips = sorted(self.SupportedTips, key=lambda x: x.Tip.Volume)

    def ValidateTransferOptions(self, Options: list[TransferOptions]):
        UnsupportedDeckLocations = list()
        UnsupportedLabware = list()
        UnsupportedLiquidClassCategories = list()

        for Opt in Options:
            SourceLabware = Opt.SourceLayoutItemInstance.Labware
            DestinationLabware = Opt.DestinationLayoutItemInstance.Labware
            if SourceLabware not in self.SupportedSourceLabwares:
                UnsupportedLabware.append(SourceLabware)
            if DestinationLabware not in self.SupportedDestinationLabwares:
                UnsupportedLabware.append(DestinationLabware)
            # Check Labware Compatibility

            SourceDeckLocation = Opt.SourceLayoutItemInstance.DeckLocation
            DestinationDeckLocation = Opt.DestinationLayoutItemInstance.DeckLocation
            if SourceDeckLocation not in self.SupportedDeckLocations:
                UnsupportedDeckLocations.append(SourceDeckLocation)
            if DestinationDeckLocation not in self.SupportedDeckLocations:
                UnsupportedDeckLocations.append(DestinationDeckLocation)
            # Check DeckLocation compatibility

            SourceLiquidClassCategory = Opt.SourceLiquidClassCategory
            DestinationLiquidClassCategory = Opt.DestinationLiquidClassCategory
            if not any(
                PipetteTip.IsLiquidClassCategorySupported(SourceLiquidClassCategory)
                for PipetteTip in self.SupportedTips
            ):
                UnsupportedLiquidClassCategories.append(SourceLiquidClassCategory)
            if not any(
                PipetteTip.IsLiquidClassCategorySupported(
                    DestinationLiquidClassCategory
                )
                for PipetteTip in self.SupportedTips
            ):
                UnsupportedLiquidClassCategories.append(DestinationLiquidClassCategory)
            # Check liquid class compatibility

    def _GetMaxTransferVolume(
        self, SourceLiquidClassCategory: str, DestinationLiquidClassCategory: str
    ) -> float:
        MaxVol = 0

        for Tip in self.SupportedTips:
            if Tip.IsLiquidClassCategorySupported(
                SourceLiquidClassCategory
            ) and Tip.IsLiquidClassCategorySupported(DestinationLiquidClassCategory):
                for LiquidClass in Tip.SupportedLiquidClassCategories[
                    SourceLiquidClassCategory
                ]:
                    if LiquidClass.MaxVolume > MaxVol:
                        MaxVol = LiquidClass.MaxVolume

                for LiquidClass in Tip.SupportedLiquidClassCategories[
                    DestinationLiquidClassCategory
                ]:
                    if LiquidClass.MaxVolume > MaxVol:
                        MaxVol = LiquidClass.MaxVolume

        return MaxVol

    def _TruncateTransferVolume(
        self, Options: TransferOptions, Volume: float
    ) -> list[TransferOptions]:
        UpdatedListedOptions = list()

        NumTransfers = ceil(Options.TransferVolume / Volume)
        TransferOptions.TransferVolume /= NumTransfers

        for _ in range(0, NumTransfers):
            UpdatedListedOptions.append(TransferOptions)

        return UpdatedListedOptions

    def _GetTip(
        self,
        SourceLiquidClassCategory: str,
        DestinationLiquidClassCategory: str,
        Volume: float,
    ) -> PipetteTip:
        PossiblePipetteTips = [
            PipetteTip
            for PipetteTip in self.SupportedTips
            if PipetteTip.IsLiquidClassCategorySupported(SourceLiquidClassCategory)
            and PipetteTip.IsLiquidClassCategorySupported(
                DestinationLiquidClassCategory
            )
        ]

        for PipetteTip in PossiblePipetteTips:
            if PipetteTip.Tip.Volume >= Volume:
                return PipetteTip

        return PossiblePipetteTips[-1]

    def _GetLiquidClass(self, LiquidClassCategory: str, Volume: float) -> str:
        Tip = self._GetTip(LiquidClassCategory, LiquidClassCategory, Volume)

        for Class in Tip.SupportedLiquidClassCategories[LiquidClassCategory]:
            if Class.MaxVolume > Volume:
                return Class.LiquidClassName

        return [
            Class.LiquidClassName
            for Class in Tip.SupportedLiquidClassCategories[LiquidClassCategory]
        ][-1]

    @abstractmethod
    def Transfer(self, ListedOptions: list[TransferOptions]):
        ...

    @abstractmethod
    def TimeToTransfer(self, ListedOptions: list[TransferOptions]):
        ...
