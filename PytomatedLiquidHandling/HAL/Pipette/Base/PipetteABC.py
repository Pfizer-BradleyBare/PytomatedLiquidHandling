from abc import abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools import AbstractClasses, LabwareAddressing

from .PipetteTip import PipetteTip

Labware.Base.LabwareNotSupportedError


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
    SourcePosition: LabwareAddressing.AlphaNumericPosition | LabwareAddressing.NumericPosition
    # This is the labware well position.
    # NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself and the HAL device will position tips accordingly
    CurrentSourceVolume: float
    SourceMixCycles: int
    SourceLiquidClassCategory: str
    DestinationLayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    DestinationPosition: LabwareAddressing.AlphaNumericPosition | LabwareAddressing.NumericPosition
    # This is the labware well position.
    # NOTE: Labware can have multiple sequences per "well." So, this assumes you choose the well itself and the HAL device will position tips accordingly
    CurrentDestinationVolume: float
    DestinationMixCycles: int
    DestinationLiquidClassCategory: str
    TransferVolume: float


@dataclass
class PipetteABC(AbstractClasses.InterfaceABC, AbstractClasses.HALObject):
    SupportedPipetteTips: list[PipetteTip]
    SupportedLabwares: list[Labware.PipettableLabware]
    SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC]

    def __post_init__(self):
        self.SupportedPipetteTips = sorted(
            self.SupportedPipetteTips, key=lambda x: x.TipInstance.MaxVolume
        )

    def ValidateTransferOptions(self, OptionsList: list[TransferOptions]):
        UnsupportedDeckLocations = list()
        UnsupportedLabware = list()
        UnsupportedLiquidClassCategories = list()

        for Options in OptionsList:
            SourceLabware = Options.SourceLayoutItemInstance.Labware
            DestinationLabware = Options.DestinationLayoutItemInstance.Labware
            if SourceLabware not in self.SupportedLabwares:
                UnsupportedLabware.append(SourceLabware)
            if DestinationLabware not in self.SupportedLabwares:
                UnsupportedLabware.append(DestinationLabware)
            # Check Labware Compatibility

            SourceDeckLocation = Options.SourceLayoutItemInstance.DeckLocation
            DestinationDeckLocation = Options.DestinationLayoutItemInstance.DeckLocation
            if SourceDeckLocation not in self.SupportedDeckLocations:
                UnsupportedDeckLocations.append(SourceDeckLocation)
            if DestinationDeckLocation not in self.SupportedDeckLocations:
                UnsupportedDeckLocations.append(DestinationDeckLocation)
            # Check DeckLocation compatibility

            SourceLiquidClassCategory = Options.SourceLiquidClassCategory
            DestinationLiquidClassCategory = Options.DestinationLiquidClassCategory
            if not any(
                PipetteTip.IsLiquidClassCategorySupported(SourceLiquidClassCategory)
                for PipetteTip in self.SupportedPipetteTips
            ):
                UnsupportedLiquidClassCategories.append(SourceLiquidClassCategory)
            if not any(
                PipetteTip.IsLiquidClassCategorySupported(
                    DestinationLiquidClassCategory
                )
                for PipetteTip in self.SupportedPipetteTips
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
            for PipetteTip in self.SupportedPipetteTips
            if PipetteTip.IsLiquidClassCategorySupported(SourceLiquidClassCategory)
            and PipetteTip.IsLiquidClassCategorySupported(
                DestinationLiquidClassCategory
            )
        ]

        for PipetteTip in PossiblePipetteTips:
            if PipetteTip.TipInstance.MaxVolume >= Volume:
                return PipetteTip

        return PossiblePipetteTips[-1]

    def _GetLiquidClass(self, LiquidClassCategory: str, Volume: float) -> str:
        return self._GetTip(
            LiquidClassCategory, LiquidClassCategory, Volume
        ).SupportedLiquidClassCategories[LiquidClassCategory]

    @abstractmethod
    def Transfer(self, ListedOptions: list[TransferOptions]):
        ...

    @abstractmethod
    def TransferTime(self, ListedOptions: list[TransferOptions]):
        ...
