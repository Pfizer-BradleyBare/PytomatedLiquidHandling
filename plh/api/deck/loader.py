from __future__ import annotations

from dataclasses import dataclass

from plh.hal import deck_location, labware, layout_item

from .container import Container, Well

__all__ = [
    "LoadedWell",
    "loaded_wells",
    "get_loaded_wells",
    "position_locks",
    "LoaderCriteria",
    "group",
    "prepare",
    "start",
    "end",
]


@dataclass
class LoadedWell:
    """A description of a loaded well and where it can be found on the deck.
    NOTE: a ```Well``` can be loaded in multiple positions and layout_items.
    """

    well: Well
    """A container well."""

    layout_item: layout_item.LayoutItemBase
    """The layout item where the well is located if loaded."""

    layout_item_well: int | str
    """The well number / position ID in the layout item where the well is located."""


loaded_wells: list[LoadedWell] = []
"""```LoadedWell``` that is actually on deck."""


def get_loaded_wells(
    well: Well,
) -> list[tuple[layout_item.LayoutItemBase, int]]:
    """Get all deck positions associated with a well."""
    ...


position_locks: set[deck_location.DeckLocationBase] = set()
"""Prevents ```deck_location``` from being stolen by other API functions.
Used only during prepare steps to ensure labware is available and ready to be loaded/unloaded."""


@dataclass
class LoaderCriteria:
    """This is how containers can be grouped when loading.
    If all the containers do not fit in the same layout_item then they will be separated but the criteria will still be valid.
    """

    containers: Container
    """All the containers that can be grouped together."""

    labware: labware.LabwareBase
    """The labware that is to be loaded with containers."""


def group(criteria: list[LoaderCriteria]) -> list[list[LoadedWell]]:
    """Take a list of ```LoaderCriteria```. The list will be grouped (list of list) based on most efficient loading then returned."""
    ...


def prepare(loaded_wells: list[LoadedWell]) -> None:
    """Depending on state of loaded wells: either the deck positions will be emptied to make room for loading,
    or the deck positions will be loaded with wells currently on deck.
    """
    ...


def start(loaded_wells: list[LoadedWell]) -> None:
    """Will move the deck locations out to the user if the HAL device (carrier_mover) is available."""
    ...


def end(loaded_wells: list[LoadedWell]) -> None:
    """Will move the deck locations back into the deck if the HAL device (carrier_mover) is available."""
    ...
