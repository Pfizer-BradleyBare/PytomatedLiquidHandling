from PytomatedLiquidHandling.API.Tools import Container
from PytomatedLiquidHandling.HAL import DeckLocation, LayoutItem, Labware

TransitionPoints: dict[str, LayoutItem.Base.LayoutItemABC] = dict()


def TransportContainer(
    Container: Container.Container,
    AcceptableDeckLocations: DeckLocation.Base.DeckLocationABC,
):
    ...


def TransportLayoutItem(
    SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
    DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
):
    if SourceLayoutItem.Labware != DestinationLayoutItem.Labware:
        raise Exception("These layout items are not compatible... WTH are you doing??")

    if (
        SourceLayoutItem.DeckLocation.TransportConfig
        != DestinationLayoutItem.DeckLocation.TransportConfig
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
