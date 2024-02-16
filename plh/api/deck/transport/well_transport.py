from __future__ import annotations

from collections import defaultdict

from plh.api.deck.container import Well
from plh.api.deck.loader import loaded_wells
from plh.hal import (
    deck_location,
)
from plh.hal import layout_item as li

from .layout_item_transport import layout_item_transport


def well_transport(
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
        layout_item_transport(source, destination)

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
