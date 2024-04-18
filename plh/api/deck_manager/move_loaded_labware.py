from __future__ import annotations

from plh.api.tools.loaded_labware import (
    LoadedLabware,
    loaded_labware_tracker,
    well_assignment_tracker,
)
from plh.hal import deck_location, layout_item
from plh.hal import transport as hal_transport

from .well import Well


def move(
    wells: list[Well],
    deck_locations: list[deck_location.DeckLocationBase],
) -> None:

    loaded_items_to_move: list[LoadedLabware] = list(
        {
            loaded_labware
            for loaded_labware in sum(
                [list(well_assignment_tracker[well]) for well in wells],
                [],
            )
            if loaded_labware.layout_item.deck_location not in deck_locations
        },
    )
    # The items we need to move are the ones that are NOT already in valid deck_locatins.
    # Only unique.

    used_deck_locations = [
        layout_item.deck_location for layout_item in loaded_labware_tracker
    ]

    possible_deck_locations = [
        deck_location
        for deck_location in deck_locations
        if deck_location not in used_deck_locations
    ]

    if len(possible_deck_locations) < len(loaded_items_to_move):
        raise RuntimeError(
            "There are not enough free deck locations to transport this container.",
        )

    possible_layout_items = sorted(
        [
            layout_item
            for layout_item in layout_item.devices.values()
            if layout_item.deck_location in possible_deck_locations
        ],
        key=lambda x: x.deck_location.identifier,
    )

    assigned_deck_locations: list[deck_location.DeckLocationBase] = []
    transport_assignments: list[tuple[LoadedLabware, layout_item.LayoutItemBase]] = []
    for loaded_item_to_move in loaded_items_to_move:
        for possible_layout_item in possible_layout_items:
            if (
                loaded_item_to_move.layout_item.labware == possible_layout_item.labware
                and possible_layout_item.deck_location not in assigned_deck_locations
            ):
                transport_assignments.append(
                    (loaded_item_to_move, possible_layout_item),
                )
                assigned_deck_locations.append(possible_layout_item.deck_location)
                break
    # For each item we need to move we need to find the right possible layout item.

    hal_transport.transport_layout_items(
        *[
            (source_loaded_item.layout_item, destination)
            for source_loaded_item, destination in transport_assignments
        ],
    )
    # Do the transports first. They are all submitted together so we can group by transport device for faster processing.

    for source_loaded_item, destination in transport_assignments:
        source_loaded_item.layout_item = destination
    # Change the tracked location of this layout item.
