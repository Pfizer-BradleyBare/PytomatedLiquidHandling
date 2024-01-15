from PytomatedLiquidHandling.API.Tools import Container

from plh.hal import (
    DeckLocation,
    Labware,
    LayoutItem,
    LayoutItems,
    TransportDevice,
)

from .Loading import GetLoadedLayoutItems, LoadedWells

TransitionPoints: dict[str, LayoutItem.Base.LayoutItemBase] = {}


def TransportContainer(
    Container: Container.Container,
    AcceptableDeckLocations: list[DeckLocation.Base.DeckLocationBase],
):
    ContainerLayoutItems = GetLoadedLayoutItems(Container)

    InUseDeckLocations = [
        LoadedWell.LayoutItem.DeckLocation for LoadedWell in LoadedWells
    ]

    PotentialDeckLocations = [
        DeckLocation
        for DeckLocation in AcceptableDeckLocations
        if DeckLocation not in InUseDeckLocations
    ]

    if len(PotentialDeckLocations) < len(LayoutItems):
        raise Exception(
            "There are not enough free deck locations to transport this container.",
        )

    PotentialLayoutItems = [
        LayoutItem
        for LayoutItem in LayoutItems.values()
        if LayoutItem.DeckLocation in PotentialDeckLocations
    ]

    for Index in range(len(ContainerLayoutItems)):
        TransportLayoutItem(ContainerLayoutItems[Index], PotentialLayoutItems[Index])


def TransportLayoutItem(
    SourceLayoutItem: LayoutItem.Base.LayoutItemBase,
    DestinationLayoutItem: LayoutItem.Base.LayoutItemBase,
):
    try:
        Device = SourceLayoutItem.DeckLocation.TransportConfig.TransportDevice

        Device.ValidateTransportOptions(SourceLayoutItem, DestinationLayoutItem)

        Device.Transport(SourceLayoutItem, DestinationLayoutItem)
        # In this case everything matches so we can just do the transport

    except* (
        TransportDevice.Base.PickupOptionsNotEqualError,
        TransportDevice.Base.TransportDevicesNotCompatibleError,
    ):
        try:
            Device = SourceLayoutItem.DeckLocation.TransportConfig.TransportDevice
            Device.ValidateTransportOptions(SourceLayoutItem, SourceLayoutItem)
        except* Labware.Base.LabwareNotSupportedError:
            raise Exception("Please god this should never happen...")

        try:
            Device = DestinationLayoutItem.DeckLocation.TransportConfig.TransportDevice
            Device.ValidateTransportOptions(
                DestinationLayoutItem,
                DestinationLayoutItem,
            )
        except* Labware.Base.LabwareNotSupportedError:
            raise Exception("Please god this should never happen...")
        # Check the labware is atleast supported...

        global TransitionPoints

        TransitionPointLayoutItem = TransitionPoints[
            SourceLayoutItem.Labware.Identifier
        ]

        TransitionPointLayoutItem.DeckLocation.TransportConfig = (
            SourceLayoutItem.DeckLocation.TransportConfig
        )

        Device = SourceLayoutItem.DeckLocation.TransportConfig.TransportDevice
        Device.Transport(SourceLayoutItem, TransitionPointLayoutItem)
        # go to transition point.

        TransitionPointLayoutItem.DeckLocation.TransportConfig = (
            DestinationLayoutItem.DeckLocation.TransportConfig
        )

        Device = SourceLayoutItem.DeckLocation.TransportConfig.TransportDevice
        Device.Transport(TransitionPointLayoutItem, DestinationLayoutItem)
        # go from transition point to destination
    # crap. Okay we need to use a transition point.
