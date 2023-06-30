from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import Carrier, DeckLocation, LayoutItem

from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from .Interface import TransportOptions
from .TransportDevice import TransportDevice


@dataclass
class TransportDeviceTracker(UniqueObjectTrackerABC[TransportDevice]):
    TransitionPointsTrackerInstance: LayoutItem.LayoutItemTracker

    def Transport(
        self, TransportOptionsTrackerInstance: TransportOptions.OptionsTracker
    ):
        DeviceLastUseIndices: dict[str, int] = dict()

        for Device in self.GetObjectsAsList():
            DeviceLastUseIndices[str(Device.UniqueIdentifier)] = 0
            Device._LastTransportFlag = False
        # Setup the devices

        for Index, Options in enumerate(
            TransportOptionsTrackerInstance.GetObjectsAsList()
        ):
            DeviceLastUseIndices[
                str(
                    Options.SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.UniqueIdentifier
                )
            ] = Index
            DeviceLastUseIndices[
                str(
                    Options.DestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.UniqueIdentifier
                )
            ] = Index
        # Figure out the last time each device is used to I can reset the last transport flag

        for Index, Options in enumerate(
            TransportOptionsTrackerInstance.GetObjectsAsList()
        ):
            SourceAwayConfig = (
                Options.SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig
            )
            DestinationAwayConfig = (
                Options.SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig
            )

            if SourceAwayConfig != DestinationAwayConfig:
                LabwareDestinationLayoutItem = (
                    self.TransitionPointsTrackerInstance.GetObjectByName(
                        Options.SourceLayoutItem.LabwareInstance.UniqueIdentifier
                    )
                )

                IntermediateDestinationTransportDeviceInstance = self.GetObjectByName(
                    LabwareDestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.UniqueIdentifier
                )
                IntermediateDestinationLayoutItem = LayoutItem.NonCoverableItem(
                    "Intermediate Destination",
                    LabwareDestinationLayoutItem.Sequence,
                    DeckLocation.DeckLocation(
                        "Intermediate Destination",
                        DeckLocation.CarrierConfig(
                            Carrier.CarrierABC("", "", 0, 0, 0, "", ""), 0
                        ),
                        DeckLocation.TransportDeviceConfig(
                            IntermediateDestinationTransportDeviceInstance.UniqueIdentifier,
                            LabwareDestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig,
                            LabwareDestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayPlaceConfig,
                            LabwareDestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig,
                            LabwareDestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayPlaceConfig,
                            # We only use the away config. TODO Explain
                        ),
                    ),
                    LabwareDestinationLayoutItem.LabwareInstance,
                )
                IntermediateDestinationTransportDeviceInstance.Transport(
                    TransportOptions.Options(
                        SourceLayoutItem=Options.SourceLayoutItem,
                        DestinationLayoutItem=IntermediateDestinationLayoutItem,
                    )
                )
                # Transport to the intermediate area from the initial source

                LabwareSourceLayoutItem = (
                    self.TransitionPointsTrackerInstance.GetObjectByName(
                        Options.SourceLayoutItem.LabwareInstance.UniqueIdentifier
                    )
                )
                IntermediateSourceTransportDeviceInstance = self.GetObjectByName(
                    LabwareSourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.UniqueIdentifier
                )

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
                            Carrier.CarrierABC("", "", 0, 0, 0, "", ""), 0
                        ),
                        DeckLocation.TransportDeviceConfig(
                            IntermediateSourceTransportDeviceInstance.UniqueIdentifier,
                            LabwareSourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig,
                            LabwareSourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayPlaceConfig,
                            LabwareSourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig,
                            LabwareSourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayPlaceConfig,
                            # We only use the away config. TODO Explain
                        ),
                    ),
                    LabwareSourceLayoutItem.LabwareInstance,
                )
                IntermediateDestinationTransportDeviceInstance.Transport(
                    TransportOptions.Options(
                        SourceLayoutItem=Options.DestinationLayoutItem,
                        DestinationLayoutItem=IntermediateSourceLayoutItem,
                    )
                )
                # Transport to the destination from the transition point
            # The two sites are not compatible. We need to use a transition point
            else:
                TransportDeviceInstance = self.GetObjectByName(
                    Options.SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.UniqueIdentifier
                )
                if (
                    DeviceLastUseIndices[str(TransportDeviceInstance.UniqueIdentifier)]
                    == Index
                ):
                    TransportDeviceInstance._LastTransportFlag = True

                TransportDeviceInstance.Transport(Options)
            # This one is easy. Sites are compatible so get on with it
