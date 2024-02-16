from __future__ import annotations

from plh.api.deck.container import Well
from plh.api.deck.loader import loaded_wells
from plh.hal import (
    deck_location,
    transport,
)
from plh.hal import layout_item as li


def wells(
    wells: list[Well],
    deck_locations: list[deck_location.DeckLocationBase],
):
    layout_items = {
        layout_item_info[0]
        for well in wells
        for layout_item_info in loaded_wells[well].layout_item_info
    }

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


def layout_item(
    source: li.LayoutItemBase,
    destination: li.LayoutItemBase,
):
    source_deck_location = source.deck_location
    destination_deck_location = destination.deck_location

    assert isinstance(source_deck_location, deck_location.TransportableDeckLocation)
    assert isinstance(
        destination_deck_location,
        deck_location.TransportableDeckLocation,
    )

    compatible_configs = (
        deck_location.TransportableDeckLocation.get_compatible_transport_configs(
            source_deck_location,
            destination_deck_location,
        )
    )

    if len(compatible_configs) > 0:

        device = compatible_configs[0][0].transport_device

        options = transport.GetPlaceOptions(
            source_layout_item=source,
            destination_layout_item=destination,
        )

        device.assert_get_place(options)

        device.get(options)

        device.place(options)
    # In this case the two locations are compatible so we can just do the transport

    else:

        for location in [
            location
            for location in deck_location.devices.values()
            if isinstance(location, deck_location.TransportableDeckLocation)
        ]:
            if location is source:
                continue
            if location is destination:
                continue

            compatible_configs = deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source,
                destination,
                location,
            )

            if len(compatible_configs) > 0:

                intermediate = [
                    layout_item
                    for layout_item in li.devices.values()
                    if layout_item.labware == source.labware
                    and layout_item.deck_location == location
                ]

                if len(intermediate) == 0:
                    continue

                layout_item(source, intermediate[0])
                layout_item(intermediate[0], destination)

                return

        raise RuntimeError("No comptible transition point found...")

    # In this case the two locations are not compatible so we can need to find a transition point.
