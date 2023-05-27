from abc import abstractmethod

from .Options import Options, OptionsTracker
from ....Tools.AbstractClasses import InterfaceABC


class TransportInterface(InterfaceABC):
    def _CheckValidity(self, OptionsInstance: Options):
        SourceLayoutItem = OptionsInstance.SourceLayoutItem

        if not SourceLayoutItem.DeckLocationInstance.SupportedLocationTransportDeviceTrackerInstance.IsTracked(
            type(self).__name__
        ):
            raise Exception(
                "This transport device is not supported for this source deck location"
            )

        if not DestinationLayoutItem.DeckLocationInstance.SupportedLocationTransportDeviceTrackerInstance.IsTracked(
            type(self).__name__
        ):
            raise Exception(
                "This transport device is not supported for this source deck location"
            )
        # Check that this is a supported transport device for the deck locations

        SourceLabwareInstance = SourceLayoutItem.LabwareInstance
        DestinationLabwareInstance = DestinationLayoutItem.LabwareInstance

        if (
            SourceLabwareInstance.GetUniqueIdentifier()
            != DestinationLabwareInstance.GetUniqueIdentifier()
        ):
            raise Exception(
                "Your source and destination labware are not the same... How did this happen???"
            )
        # Check that the labware is the same for both source and destination

        if not self.TransportableLabwareTrackerInstance.IsTracked(
            SourceLabwareInstance.GetUniqueIdentifier()
        ):
            raise Exception("The labware is not supported by this transport device")
        # Check that the transport device can move this labware

        SourceTransportableLabware = (
            self.TransportableLabwareTrackerInstance.GetObjectByName(
                SourceLabwareInstance.GetUniqueIdentifier()
            )
        )

        GetPlateOptionsInstance = GripperDriver.GetPlate.Options(
            self.GripperToolSequence,
            SourceLayoutItem.Sequence,
            SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
            - SourceTransportableLabware.TransportParametersInstance.CloseOffset,
            SourceLayoutItem.LabwareInstance.DimensionsInstance.ShortSide
            + SourceTransportableLabware.TransportParametersInstance.OpenOffset,
        )
        GetPlateOptionsInstance.GripHeight = (
            SourceTransportableLabware.TransportParametersInstance.PickupHeight
        )

        try:
            GripperDriver.GetPlate.Command(GetPlateOptionsInstance, True).Execute()

        except:
            ...

        try:
            GripperDriver.PlacePlate.Command(
                GripperDriver.PlacePlate.Options(
                    DestinationLayoutItem.Sequence,
                ),
                True,
            ).Execute()

        except:
            ...

    @abstractmethod
    def TransportSingle(self, OptionsInstance: Options):
        ...

    @abstractmethod
    def TransportMultiple(self, OptionsTrackerInstance: OptionsTracker):
        ...
