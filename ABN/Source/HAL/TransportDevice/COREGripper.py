from typing import cast

from ...Driver.Handler.DriverHandler import DriverHandler
from ...Driver.Transport.Gripper import (
    GetPlateCommand,
    GetPlateOptions,
    PlacePlateCommand,
    PlacePlateOptions,
)
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Layout import LayoutItem
from .BaseTransportDevice import (
    TransportableLabwareTracker,
    TransportDevice,
    TransportDevices,
)


class COREGripper(TransportDevice):
    def __init__(
        self,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
        GripperToolSequence: str,
    ):
        self.GripperToolSequence: str = GripperToolSequence
        TransportDevice.__init__(
            self, TransportDevices.COREGripper, TransportableLabwareTrackerInstance
        )

    def Initialize(self):
        pass

    def Deinitialize(self):
        pass

    def Transport(
        self, SourceLayoutItem: LayoutItem, DestinationLayoutItem: LayoutItem
    ):
        __DriverHandlerInstance: DriverHandler = cast(
            DriverHandler, HandlerRegistry.GetObjectByName("Driver")
        )

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

        if SourceLabwareInstance.GetName() != DestinationLabwareInstance.GetName():
            raise Exception(
                "Your source and destination labware are not the same... How did this happen???"
            )
        # Check that the labware is the same for both source and destination

        if not self.TransportableLabwareTrackerInstance.IsTracked(
            SourceLabwareInstance.GetName()
        ):
            raise Exception("The labware is not supported by this transport device")
        # Check that the transport device can move this labware

        SourceTransportableLabware = (
            self.TransportableLabwareTrackerInstance.GetObjectByName(
                SourceLabwareInstance.GetName()
            )
        )

        GetPlateOptionsInstance = GetPlateOptions(
            "",
            self.GripperToolSequence,
            SourceLayoutItem.Sequence,
            SourceLayoutItem.LabwareInstance.Dimensions.ShortSide
            - SourceTransportableLabware.TransportParametersInstance.CloseOffset,
            SourceLayoutItem.LabwareInstance.Dimensions.ShortSide
            + SourceTransportableLabware.TransportParametersInstance.OpenOffset,
        )
        GetPlateOptionsInstance.GripHeight = (
            SourceTransportableLabware.TransportParametersInstance.PickupHeight
        )

        __DriverHandlerInstance.ExecuteCommand(
            GetPlateCommand(
                "",
                True,
                GetPlateOptionsInstance,
            )
        )

        __DriverHandlerInstance.ExecuteCommand(
            PlacePlateCommand(
                "",
                True,
                PlacePlateOptions(
                    "",
                    DestinationLayoutItem.Sequence,
                ),
            )
        )

    def GetConfigKeys(self) -> list[str]:
        return []
