from __future__ import annotations

from plh.api.container import Well
from plh.api.tools.loaded_labware import (
    well_assignment_tracker,
)
from plh.implementation import deck_location

from .move_loaded_labware import move_loaded_labware


def move_container(
    wells: list[Well],
    deck_locations: list[deck_location.DeckLocationBase],
) -> None:

    move_loaded_labware(
        sum(
            [list(well_assignment_tracker[well]) for well in wells],
            [],
        ),
        deck_locations,
    )
