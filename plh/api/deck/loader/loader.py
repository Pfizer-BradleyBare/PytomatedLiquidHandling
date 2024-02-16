from __future__ import annotations

from dataclasses import dataclass
from math import ceil

from plh.api.deck.container import Well
from plh.hal import carrier_loader, labware, layout_item

__all__ = [
    "loaded_wells",
    "Location",
    "Criteria",
    "group",
    "prepare",
    "start",
    "end",
]


@dataclass
class Location:
    """A location on the deck where physical items will be loaded or unloaded."""

    well: Well
    """A container well."""

    layout_item: layout_item.LayoutItemBase
    """The layout item where the well is located if loaded/unloaded."""

    layout_item_well: int | str
    """The physical well in the layout item."""


loaded_wells: dict[Well, list[tuple[layout_item.LayoutItemBase, list[int | str]]]] = {}
"""```Well``` that is actually present on the deck.
NOTE: depending on the volume needed for a well it can span mutliple layout items / physical wells."""


@dataclass
class Criteria:
    """This is how wells can be grouped when loading.
    If all the wells do not fit in the same layout_item then they will be separated but the criteria will still be valid.
    Well order will also be preserved.
    """

    wells: list[Well]
    """All the containers that can be grouped together."""

    labware: labware.LabwareBase
    """The labware that is to be loaded with containers."""


def group(criteria: list[Criteria]) -> list[list[Location]]:
    """Take a list of ```LoaderCriteria```. The list will be grouped (list of list) based on most efficient loading (similar carrier) then returned."""
    if not all(
        isinstance(criterion.labware, labware.PipettableLabware)
        for criterion in criteria
    ):
        raise TypeError("All labware must be of type PipettableLabware.")

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

    criteria_num_labware: list[tuple[Criteria, int]] = []

    for criterion in criteria:

        assert isinstance(criterion.labware, labware.PipettableLabware)
        # Already checked above.

        num_physical_wells = 0

        for well in criterion.wells:
            num_physical_wells += ceil(
                well.get_total_volume() / criterion.labware.well_definition.max_volume,
            )

        criteria_num_labware.append(
            (
                criterion,
                ceil(num_physical_wells / criterion.labware.layout.total_positions()),
            ),
        )
        # How many of each labware do we need for all containers?

        print(
            criteria_num_labware[0][1],
            criteria_num_labware[0][0].wells[0].get_total_volume(),
        )


def prepare(locations: list[Location]) -> None:
    """Depending on state of loaded wells: either the deck positions will be emptied to make room for loading
    or the deck positions will be loaded with wells currently on deck.
    """
    ...


def start(locations: list[Location]) -> None:
    """Will move the deck locations out to the user if the HAL device (carrier_mover) is available."""
    ...


def end(locations: list[Location]) -> None:
    """Will move the deck locations back into the deck if the HAL device (carrier_mover) is available."""
    ...
