from abc import abstractmethod
from dataclasses import dataclass

from pydantic import field_validator

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools import AbstractClasses

from .PipetteTip import PipetteTip


@dataclass
class LiquidClassCategoryNotSupportedError(BaseException):
    """HAL device does not support your Labware. This can be thrown for any LayoutItem inputs.

    Attributes:
    Categories: List of string category names that were not supported
    """

    Categories: list[str]


@dataclass(kw_only=True)
class TransferOptions(OptionsABC):
    SourceLayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    SourcePosition: str | int
    # This is the labware well position.
    # NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself and the HAL device will position tips accordingly
    CurrentSourceVolume: float
    SourceMixCycles: int
    SourceLiquidClassCategory: str
    DestinationLayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    DestinationPosition: str | int
    # This is the labware well position.
    # NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself and the HAL device will position tips accordingly
    CurrentDestinationVolume: float
    DestinationMixCycles: int
    DestinationLiquidClassCategory: str
    TransferVolume: float


@dataclass(kw_only=True)
class ListedTransferOptions(list[TransferOptions]):
    ...


class PipetteABC(AbstractClasses.Interface, AbstractClasses.HALDevice):
    SupportedTips: list[PipetteTip]
    SupportedLabwares: list[Labware.PipettableLabware]
    SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC]

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

    @field_validator("SupportedLabwares", mode="before")
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

    def __post_init__(self):
        self.SupportedTips = sorted(self.SupportedTips, key=lambda x: x.Tip.Volume)

    def ValidateTransferOptions(self, Options: list[TransferOptions]):
        UnsupportedDeckLocations = list()
        UnsupportedLabware = list()
        UnsupportedLiquidClassCategories = list()

        for Opt in Options:
            SourceLabware = Opt.SourceLayoutItemInstance.Labware
            DestinationLabware = Opt.DestinationLayoutItemInstance.Labware
            if SourceLabware not in self.SupportedLabwares:
                UnsupportedLabware.append(SourceLabware)
            if DestinationLabware not in self.SupportedLabwares:
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
        return self._GetTip(
            LiquidClassCategory, LiquidClassCategory, Volume
        ).SupportedLiquidClassCategories[LiquidClassCategory]

    @abstractmethod
    def Transfer(self, ListedOptions: ListedTransferOptions):
        ...

    @abstractmethod
    def TransferTime(self, ListedOptions: ListedTransferOptions):
        ...
