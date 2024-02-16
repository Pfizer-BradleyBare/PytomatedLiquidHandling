from __future__ import annotations

from dataclasses import dataclass
from math import ceil

from plh.hal import carrier_loader, labware, layout_item

from .container import Well

__all__ = [
    "loaded_wells",
    "Location",
    "Criteria",
    "group",
    "prepare",
    "start",
    "end",
]

loaded_wells: dict[Well, list[tuple[layout_item.LayoutItemBase, int | str]]] = {}
"""```Well``` that is actually present on the deck.
NOTE: depending on the volume needed for a well it can span mutliple layout items / physical wells."""


@dataclass
class Location:
    """A description of a loaded well and where it can be found on the deck.
    NOTE: a ```Well``` can be loaded in multiple positions and layout_items.
    """

    well: Well
    """A container well."""

    layout_item_info: list[tuple[layout_item.LayoutItemBase, int]]
    """The layout items where the well is located if loaded and the wells it is located in."""

    layout_item_well: int | str
    """The well number / position ID in the layout item where the well is located."""


@dataclass
class Criteria:
    """This is how containers can be grouped when loading.
    If all the containers do not fit in the same layout_item then they will be separated but the criteria will still be valid.
    """

    containers: list[Container]
    """All the containers that can be grouped together."""

    labware: labware.PipettableLabware
    """The labware that is to be loaded with containers."""


def group(criteria: list[LoaderCriteria]) -> list[list[LoaderLocation]]:
    """Take a list of ```LoaderCriteria```. The list will be grouped (list of list) based on most efficient loading (similar carrier) then returned."""
    loadable_carriers = sum(
        [loader.supported_carriers for loader in carrier_loader.devices.values()],
        [],
    )
    # We only use carriers that have an associated carrier_loader for loading.

    loadable_layout_items = [
        layout_item
        for layout_item in layout_item.devices.values()
        if layout_item.deck_location.carrier_config.carrier in loadable_carriers
    ]
    # These are all the potential layout items we can use to load.

    labwares = [layout_item.labware for layout_item in loadable_layout_items]

    labware_availability = dict(
        sorted(
            {labware: labwares.count(labware) for labware in set(labwares)}.items(),
            key=lambda x: x[1],
        ),
    )
    # get number of available labware positions. We want to try to load labware with the least positions first.

    criteria = [
        item[0]
        for item in sorted(
            [
                (criterion, labware_availability[criterion.labware])
                for criterion in criteria
            ],
            key=lambda x: x[1],
        )
    ]
    # sort criteria based on number of available labware.

    criteria_num_labware: list[tuple[LoaderCriteria, int]] = []

    for criterion in criteria:
        labware = criterion.labware

        for container in criterion.containers:
            num_physical_wells = 0

            for well in container.wells:
                num_physical_wells += ceil(
                    well.get_total_volume() / labware.well_definition.max_volume,
                )

        criteria_num_labware.append(
            (criterion, ceil(num_physical_wells / labware.layout.total_positions())),
        )
    # How many of each labware do we need for all containers?


def prepare(locations: list[LoaderLocation]) -> None:
    """Depending on state of loaded wells: either the deck positions will be emptied to make room for loading
    or the deck positions will be loaded with wells currently on deck.
    """
    ...


def start(locations: list[LoaderLocation]) -> None:
    """Will move the deck locations out to the user if the HAL device (carrier_mover) is available."""
    ...


def end(locations: list[LoaderLocation]) -> None:
    """Will move the deck locations back into the deck if the HAL device (carrier_mover) is available."""
    ...
