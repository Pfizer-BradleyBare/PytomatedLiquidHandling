from typing import Callable

from ...Driver.NOP import NOPCommand
from ...Driver.Tools import Command, CommandTracker
from ...Driver.Transport.Gripper import (
    GetPlateCommand,
    GetPlateOptions,
    PlacePlateCommand,
    PlacePlateOptions,
)
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

    def Initialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            NOPCommand(
                "COREGripper Initialize NOP",
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def Deinitialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            NOPCommand(
                "COREGripper Deinitialize NOP",
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def Transport(
        self,
        SourceLayoutItem: LayoutItem,
        DestinationLayoutItem: LayoutItem,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

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

        ReturnCommandTracker.ManualLoad(
            GetPlateCommand(
                "",
                True,
                GetPlateOptionsInstance,
            )
        )

        ReturnCommandTracker.ManualLoad(
            PlacePlateCommand(
                "",
                True,
                PlacePlateOptions(
                    "",
                    DestinationLayoutItem.Sequence,
                ),
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def GetConfigKeys(self) -> list[str]:
        return []