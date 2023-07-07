from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import Labware, LayoutItem

from ....Tools.AbstractClasses import UniqueObjectABC
from ...Tools.AbstractClasses import InterfaceABC
from . import DeckLocationTransportConfigTracker
from .Interface import TransportOptions


@dataclass
class TransportDevice(InterfaceABC, UniqueObjectABC):
    DeckLocationTransportConfigTrackerInstance: DeckLocationTransportConfigTracker
    SupportedLabwareTrackerInstance: Labware.LabwareTracker
    _LastTransportFlag: bool = field(init=False, default=True)

    def _CheckIsValid(self, TransportOptionsInstance: TransportOptions.Options):
        SourceLayoutItem = TransportOptionsInstance.SourceLayoutItem
        DestinationLayoutItem = TransportOptionsInstance.DestinationLayoutItem

        if not self.DeckLocationTransportConfigTrackerInstance.IsTracked(
            SourceLayoutItem.DeckLocationInstance.UniqueIdentifier
        ):
            raise Exception(
                "This transport device is not supported for this source deck location"
            )

        if not self.DeckLocationTransportConfigTrackerInstance.IsTracked(
            DestinationLayoutItem.DeckLocationInstance.UniqueIdentifier
        ):
            raise Exception(
                "This transport device is not supported for this destination deck location"
            )
        # Check that this is a supported transport device for the deck locations

        if (
            self.DeckLocationTransportConfigTrackerInstance.GetObjectByName(
                SourceLayoutItem.DeckLocationInstance.UniqueIdentifier
            ).GetConfig
            != self.DeckLocationTransportConfigTrackerInstance.GetObjectByName(
                DestinationLayoutItem.DeckLocationInstance.UniqueIdentifier
            ).GetConfig
        ):
            raise Exception(
                "Source and destination extra options are not compatible. Use a transition point to properly orient."
            )
        # I am comparing away configs because the way we pickup before the transfer must be the same orientation
        # This indicates a seamless transition from source home to destination home configs

        SourceLabwareInstance = SourceLayoutItem.LabwareInstance
        DestinationLabwareInstance = DestinationLayoutItem.LabwareInstance

        if (
            SourceLabwareInstance.UniqueIdentifier
            != DestinationLabwareInstance.UniqueIdentifier
        ):
            raise Exception(
                "Your source and destination labware are not the same... How did this happen???"
            )
        # Check that the labware is the same for both source and destination

        if not self.SupportedLabwareTrackerInstance.IsTracked(
            SourceLabwareInstance.UniqueIdentifier
        ):
            raise Exception("The labware is not supported by this transport device")
        # Check that the transport device can move this labware

        if not type(SourceLayoutItem) == type(DestinationLayoutItem):
            if (
                type(SourceLayoutItem) == LayoutItem.CoverableItem
                and type(DestinationLayoutItem) == LayoutItem.NonCoverableItem
                and SourceLayoutItem.IsCovered == True
            ):
                raise Exception(
                    "Source and Destination are not compatible layout items"
                )

    @abstractmethod
    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        ...
