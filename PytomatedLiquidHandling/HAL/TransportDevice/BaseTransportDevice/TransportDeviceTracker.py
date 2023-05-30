from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from .TransportDevice import TransportDevice
from .Interface import TransportOptions
from ...LayoutItem import LayoutItemTracker, NonCoverablePosition
from ...DeckLocation import DeckLocation, TransportDeviceConfig


class TransportDeviceTracker(UniqueObjectTrackerABC[TransportDevice]):
    def __init__(self, TransitionPointsTrackerInstance: LayoutItemTracker):
        UniqueObjectTrackerABC.__init__(self)
        self.TransitionPointsTrackerInstance: LayoutItemTracker = (
            TransitionPointsTrackerInstance
        )

    def Transport(
        self, TransportOptionsTrackerInstance: TransportOptions.OptionsTracker
    ):
        DeviceLastUseIndices: dict[str, int] = dict()

        for Device in self.GetObjectsAsList():
            DeviceLastUseIndices[str(Device.GetUniqueIdentifier())] = 0
            Device._LastTransportFlag = False
        # Setup the devices

        for Index, Options in enumerate(
            TransportOptionsTrackerInstance.GetObjectsAsList()
        ):
            DeviceLastUseIndices[
                str(
                    Options.SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.GetUniqueIdentifier()
                )
            ] = Index
            DeviceLastUseIndices[
                str(
                    Options.DestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.GetUniqueIdentifier()
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
                        Options.SourceLayoutItem.LabwareInstance.GetUniqueIdentifier()
                    )
                )

                IntermediateDestinationTransportDeviceInstance = (
                    LabwareDestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.TransportDeviceInstance
                )
                IntermediateDestinationLayoutItem = NonCoverablePosition(
                    "Intermediate Destination",
                    LabwareDestinationLayoutItem.Sequence,
                    LabwareDestinationLayoutItem.LabwareInstance,  # type: ignore
                    DeckLocation(
                        "Intermediate Destination",
                        TransportDeviceConfig(
                            IntermediateDestinationTransportDeviceInstance,
                            LabwareDestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig,
                            LabwareDestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayPlaceConfig,
                            LabwareDestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig,
                            LabwareDestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayPlaceConfig,
                            # We only use the away config. TODO Explain
                        ),
                    ),
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
                        Options.SourceLayoutItem.LabwareInstance.GetUniqueIdentifier()
                    )
                )
                IntermediateSourceTransportDeviceInstance = (
                    LabwareSourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.TransportDeviceInstance
                )

                if (
                    DeviceLastUseIndices[
                        str(
                            IntermediateSourceTransportDeviceInstance.GetUniqueIdentifier()
                        )
                    ]
                    == Index
                ):
                    IntermediateSourceTransportDeviceInstance._LastTransportFlag = True

                IntermediateSourceLayoutItem = NonCoverablePosition(
                    "Intermediate Source",
                    LabwareSourceLayoutItem.Sequence,
                    LabwareSourceLayoutItem.LabwareInstance,  # type: ignore
                    DeckLocation(
                        "Intermediate Source",
                        TransportDeviceConfig(
                            IntermediateSourceTransportDeviceInstance,
                            LabwareSourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig,
                            LabwareSourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayPlaceConfig,
                            LabwareSourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayGetConfig,
                            LabwareSourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.AwayPlaceConfig,
                            # We only use the away config. TODO Explain
                        ),
                    ),
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
                TransportDeviceInstance = (
                    Options.SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.TransportDeviceInstance
                )
                if (
                    DeviceLastUseIndices[
                        str(TransportDeviceInstance.GetUniqueIdentifier())
                    ]
                    == Index
                ):
                    TransportDeviceInstance._LastTransportFlag = True

                TransportDeviceInstance.Transport(Options)
            # This one is easy. Sites are compatible so get on with it
