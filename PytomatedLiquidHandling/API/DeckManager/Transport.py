from PytomatedLiquidHandling.API.Tools import Container
from PytomatedLiquidHandling.HAL import DeckLocation, LayoutItem, LayoutItems

from .Loading import GetLoadedLayoutItems, LoadedWells

TransitionPoints: dict[str, LayoutItem.Base.LayoutItemABC] = dict()


def TransportContainer(
    Container: Container.Container,
    AcceptableDeckLocations: list[DeckLocation.Base.DeckLocationABC],
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
            "There are not enough free deck locations to transport this container."
        )

    PotentialLayoutItems = [
        LayoutItem
        for LayoutItem in LayoutItems.values()
        if LayoutItem.DeckLocation in PotentialDeckLocations
    ]

    for Index in range(0, len(ContainerLayoutItems)):
        TransportLayoutItem(ContainerLayoutItems[Index], PotentialLayoutItems[Index])


def TransportLayoutItem(
    SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
    DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
):
    if SourceLayoutItem.Labware != DestinationLayoutItem.Labware:
        raise Exception("These layout items are not compatible... WTH are you doing??")

    if (
        SourceLayoutItem.DeckLocation.TransportConfig.PickupOptions
        != DestinationLayoutItem.DeckLocation.TransportConfig.PickupOptions
    ):
        global TransitionPoints

        TransitionPointLayoutItem = TransitionPoints[
            SourceLayoutItem.Labware.Identifier
        ]

        TransitionPointLayoutItem.DeckLocation.TransportConfig = (
            SourceLayoutItem.DeckLocation.TransportConfig
        )

        TransportDevice = SourceLayoutItem.DeckLocation.TransportConfig.TransportDevice
        TransportDevice.Transport(
            TransportDevice.Options(
                SourceLayoutItem=SourceLayoutItem,
                DestinationLayoutItem=TransitionPointLayoutItem,
            )
        )
        # go to transition point.

        TransitionPointLayoutItem.DeckLocation.TransportConfig = (
            DestinationLayoutItem.DeckLocation.TransportConfig
        )

        TransportDevice = SourceLayoutItem.DeckLocation.TransportConfig.TransportDevice
        TransportDevice.Transport(
            TransportDevice.Options(
                SourceLayoutItem=TransitionPointLayoutItem,
                DestinationLayoutItem=DestinationLayoutItem,
            )
        )
        # go from transition point to destination

    # crap. Okay we need to use a transition point.
    else:
        TransportDevice = SourceLayoutItem.DeckLocation.TransportConfig.TransportDevice
        TransportDevice.Transport(
            TransportDevice.Options(
                SourceLayoutItem=SourceLayoutItem,
                DestinationLayoutItem=DestinationLayoutItem,
            )
        )
    # Hooray we can just do the transport!
    # Are these bad boys compatible? Meaning are the pickup options similar...
