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
    CurrentSourceComposition: float | list[tuple[str, float]]
    SourceMixCycles: int
    SourceLiquidClassCategory: str
    DestinationLayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    DestinationPosition: str | int
    # This is the labware well position.
    # NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself and the HAL device will position tips accordingly
    CurrentDestinationComposition: float | list[tuple[str, float]]
    DestinationMixCycles: int
    DestinationLiquidClassCategory: str
    TransferVolume: float

    def __post_init__(self):
        if isinstance(self.CurrentSourceComposition, float):
            self.CurrentSourceComposition = [
                ("Source N/A", self.CurrentSourceComposition)
            ]

        if isinstance(self.CurrentDestinationComposition, float):
            self.CurrentDestinationComposition = [
                ("Destination N/A", self.CurrentDestinationComposition)
            ]

        # We want to input to be a composition. If the user doesn't care then we will


@dataclass(kw_only=True)
class ListedTransferOptions(list[TransferOptions]):
    ...


class PipetteABC(AbstractClasses.Interface, AbstractClasses.HALDevice):
    SupportedTips: list[PipetteTip]
    SupportedLabwares: list[Labware.PipettableLabware]
    SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC]

    @field_validator("SupportedTips", mode="before")
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
                PipetteTip.IsLiquidClassCategorySupported(
                    SourceLiquidClassCategory, Opt.TransferVolume
                )
                for PipetteTip in self.SupportedTips
            ):
                UnsupportedLiquidClassCategories.append(SourceLiquidClassCategory)
            if not any(
                PipetteTip.IsLiquidClassCategorySupported(
                    DestinationLiquidClassCategory, Opt.TransferVolume
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
            if PipetteTip.IsLiquidClassCategorySupported(
                SourceLiquidClassCategory, Volume
            )
            and PipetteTip.IsLiquidClassCategorySupported(
                DestinationLiquidClassCategory, Volume
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
    def Transfer(
        self, ListedOptions: ListedTransferOptions | list[ListedTransferOptions]
    ):
        ...

    @abstractmethod
    def TransferTime(
        self, ListedOptions: ListedTransferOptions | list[ListedTransferOptions]
    ):
        ...
