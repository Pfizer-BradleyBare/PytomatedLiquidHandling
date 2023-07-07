from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import Carrier, DeckLocation, LayoutItem

from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from . import DeckLocationTransportConfig, TransportDevice
from .Interface import TransportOptions


@dataclass
class TransportDeviceTracker(UniqueObjectTrackerABC[TransportDevice]):
    TransitionPointsTrackerInstance: LayoutItem.LayoutItemTracker

    def Transport(
        self, TransportOptionsTrackerInstance: TransportOptions.OptionsTracker
    ):
        DeviceLastUseIndices: dict[str | int, int] = dict()

        for Device in self.GetObjectsAsList():
            DeviceLastUseIndices[str(Device.UniqueIdentifier)] = 0
            Device._LastTransportFlag = False
        # Setup the devices

        for Index, Options in enumerate(
            TransportOptionsTrackerInstance.GetObjectsAsList()
        ):
            for TransportDevice in self.GetObjectsAsList():
                if TransportDevice.DeckLocationTransportConfigTrackerInstance.IsTracked(
                    Options.SourceLayoutItem.DeckLocationInstance.UniqueIdentifier
                ):
                    DeviceLastUseIndices[TransportDevice.UniqueIdentifier] = Index

                if TransportDevice.DeckLocationTransportConfigTrackerInstance.IsTracked(
                    Options.DestinationLayoutItem.DeckLocationInstance.UniqueIdentifier
                ):
                    DeviceLastUseIndices[TransportDevice.UniqueIdentifier] = Index
        # Figure out the last time each device is used to I can reset the last transport flag

        for Index, Options in enumerate(
            TransportOptionsTrackerInstance.GetObjectsAsList()
        ):
            SourceTransportConfigInstance = None
            SourceTransportDevice = None
            DestinationTransportConfigInstance = None
            DestinationTransportDevice = None

            for TransportDevice in self.GetObjectsAsList():
                if TransportDevice.DeckLocationTransportConfigTrackerInstance.IsTracked(
                    Options.SourceLayoutItem.DeckLocationInstance.UniqueIdentifier
                ):
                    SourceTransportConfigInstance = TransportDevice.DeckLocationTransportConfigTrackerInstance.GetObjectByName(
                        Options.SourceLayoutItem.DeckLocationInstance.UniqueIdentifier
                    )
                    SourceTransportDevice = TransportDevice

                if TransportDevice.DeckLocationTransportConfigTrackerInstance.IsTracked(
                    Options.DestinationLayoutItem.DeckLocationInstance.UniqueIdentifier
                ):
                    DestinationTransportConfigInstance = TransportDevice.DeckLocationTransportConfigTrackerInstance.GetObjectByName(
                        Options.DestinationLayoutItem.DeckLocationInstance.UniqueIdentifier
                    )
                    DestinationTransportDevice = TransportDevice
            # Get our transport config for this transfer

            if SourceTransportConfigInstance is None:
                raise Exception("I hope this never happens")
            if DestinationTransportConfigInstance is None:
                raise Exception("I hope this never happens")
            if SourceTransportDevice is None:
                raise Exception("I hope this never happens")
            if DestinationTransportDevice is None:
                raise Exception("I hope this never happens")

            if (
                SourceTransportConfigInstance.GetConfig
                != DestinationTransportConfigInstance.GetConfig
            ):
                LabwareDestinationLayoutItem = (
                    self.TransitionPointsTrackerInstance.GetObjectByName(
                        Options.SourceLayoutItem.LabwareInstance.UniqueIdentifier
                    )
                )
                IntermediateDestinationTransportDeviceInstance = SourceTransportDevice

                IntermediateDestinationLayoutItem = LayoutItem.NonCoverableItem(
                    "Intermediate Destination",
                    LabwareDestinationLayoutItem.Sequence,
                    DeckLocation.DeckLocation(
                        "Intermediate Destination",
                        DeckLocation.CarrierConfig(
                            Carrier.CarrierABC("", 0, 0, 0, "", ""), 0
                        ),
                    ),
                    LabwareDestinationLayoutItem.LabwareInstance,
                )

                DeckLocationTransportConfigInstance = DeckLocationTransportConfig(
                    "Intermediate Destination",
                    SourceTransportConfigInstance.GetConfig,
                    SourceTransportConfigInstance.PlaceConfig,
                )

                IntermediateDestinationTransportDeviceInstance.DeckLocationTransportConfigTrackerInstance.LoadSingle(
                    DeckLocationTransportConfigInstance
                )

                IntermediateDestinationTransportDeviceInstance.Transport(
                    TransportOptions.Options(
                        SourceLayoutItem=Options.SourceLayoutItem,
                        DestinationLayoutItem=IntermediateDestinationLayoutItem,
                    )
                )
                # Transport to the intermediate area from the initial source

                IntermediateDestinationTransportDeviceInstance.DeckLocationTransportConfigTrackerInstance.UnloadSingle(
                    DeckLocationTransportConfigInstance
                )

                LabwareSourceLayoutItem = (
                    self.TransitionPointsTrackerInstance.GetObjectByName(
                        Options.SourceLayoutItem.LabwareInstance.UniqueIdentifier
                    )
                )
                IntermediateSourceTransportDeviceInstance = DestinationTransportDevice

                if (
                    DeviceLastUseIndices[
                        str(IntermediateSourceTransportDeviceInstance.UniqueIdentifier)
                    ]
                    == Index
                ):
                    IntermediateSourceTransportDeviceInstance._LastTransportFlag = True

                IntermediateSourceLayoutItem = LayoutItem.NonCoverableItem(
                    "Intermediate Source",
                    LabwareSourceLayoutItem.Sequence,
                    DeckLocation.DeckLocation(
                        "Intermediate Source",
                        DeckLocation.CarrierConfig(
                            Carrier.CarrierABC("", 0, 0, 0, "", ""), 0
                        ),
                    ),
                    LabwareSourceLayoutItem.LabwareInstance,
                )

                DeckLocationTransportConfigInstance = DeckLocationTransportConfig(
                    "Intermediate Source",
                    DestinationTransportConfigInstance.GetConfig,
                    DestinationTransportConfigInstance.PlaceConfig,
                )

                IntermediateDestinationTransportDeviceInstance.DeckLocationTransportConfigTrackerInstance.LoadSingle(
                    DeckLocationTransportConfigInstance
                )

                IntermediateDestinationTransportDeviceInstance.Transport(
                    TransportOptions.Options(
                        SourceLayoutItem=Options.DestinationLayoutItem,
                        DestinationLayoutItem=IntermediateSourceLayoutItem,
                    )
                )
                # Transport to the destination from the transition point

                IntermediateDestinationTransportDeviceInstance.DeckLocationTransportConfigTrackerInstance.UnloadSingle(
                    DeckLocationTransportConfigInstance
                )

            # The two sites are not compatible. We need to use a transition point
            else:
                if SourceTransportDevice != DestinationTransportDevice:
                    raise Exception("Something went wrong here...")

                TransportDeviceInstance = SourceTransportDevice
                if (
                    DeviceLastUseIndices[str(TransportDeviceInstance.UniqueIdentifier)]
                    == Index
                ):
                    TransportDeviceInstance._LastTransportFlag = True

                TransportDeviceInstance.Transport(Options)
            # This one is easy. Sites are compatible so get on with it
