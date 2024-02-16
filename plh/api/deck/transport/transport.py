from __future__ import annotations

from collections import defaultdict

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
) -> None:
    layout_items: dict[li.LayoutItemBase, list[Well]] = defaultdict(list)

    for well in wells:
        for layout_item_info in loaded_wells[well]:
            layout_items[layout_item_info[0]].append(well)
    # multiple wells can be in a single layout item. Let's get the unique ones.
    # Some layout items may already be in an acceptable location. Skip those.

    used_deck_locations = [layout_item.deck_location for layout_item in layout_items]

    possible_deck_locations = [
        deck_location
        for deck_location in deck_locations
        if deck_location not in used_deck_locations
    ]

    if len(possible_deck_locations) < len(layout_items):
        raise RuntimeError(
            "There are not enough free deck locations to transport this container.",
        )

    possible_layout_items = [
        layout_item
        for layout_item in li.devices.values()
        if layout_item.deck_location in possible_deck_locations
    ]

    for (source, wells), destination in zip(
        layout_items.items(),
        possible_layout_items,
    ):
        layout_item(source, destination)

        for well in wells:
            loaded_wells[well] = [
                (
                    (destination, layout_item_info[1])
                    if layout_item_info[0] is source
                    else layout_item_info
                )
                for layout_item_info in loaded_wells[well]
            ]
        # Change the tracked location of this layout item.


def layout_item(
    source: li.LayoutItemBase,
    destination: li.LayoutItemBase,
) -> None:
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
