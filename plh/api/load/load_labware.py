from __future__ import annotations

from dataclasses import dataclass, field
from itertools import groupby

from plh.api import container
from plh.hal import carrier_loader, labware, layout_item


@dataclass
class LoadedLabware:
    """Labware they is loaded on the deck or is in the process of being loaded on deck."""

    labware: labware.LabwareBase
    """The labware type."""

    layout_item: layout_item.LayoutItemBase
    """Where it is or will be on deck."""

    well_assignments: dict[int, container.Well | None] = field(init=False)
    """Wells that have been assigned to the container."""

    def __post_init__(self: LoadedLabware) -> None:
        self.well_assignments = dict.fromkeys(
            range(1, self.labware.layout.total_positions() + 1),
        )


def group(labwares: list[labware.LabwareBase]) -> list[list[LoadedLabware]]:
    """Takes a list of labware and groups it by carrier for loading."""
    loadable_carriers = sum(
        [loader.supported_carriers for loader in carrier_loader.devices.values()],
        [],
    )
    # We only use carriers that have an associated carrier_loader for loading.

    loadable_layout_items = sorted(
        [
            layout_item
            for layout_item in layout_item.devices.values()
            if layout_item.deck_location.carrier_config.carrier in loadable_carriers
        ],
        key=lambda x: x.deck_location.identifier,
    )
    # These are all the potential layout items we can use to load.

    required_labware = {labware: labwares.count(labware) for labware in set(labwares)}
    # get number of each labware we need to load.

    loadable_labware = [
        layout_item.labware
        for layout_item in loadable_layout_items
        if layout_item.labware in required_labware
    ]

    available_labware = dict(
        sorted(
            {
                labware: loadable_labware.count(labware)
                for labware in set(loadable_labware)
            }.items(),
            key=lambda x: x[1],
        ),
    )
    # get number of available labware positions sorted from least available to most available.

    loaded_layout_items: list[layout_item.LayoutItemBase] = []

    for labware, num_available in available_labware.items():
        num_to_load = required_labware[labware]

        if num_to_load > num_available:
            raise RuntimeError("Not enough labware available!")

        loaded_layout_items += [
            layout_item
            for layout_item in loadable_layout_items
            if layout_item.labware is labware
            and layout_item.deck_location
            not in [item.deck_location for item in loaded_layout_items]
        ][:num_to_load]
    # Try to load it.

    return [
        [
            LoadedLabware(layout_item.labware, layout_item)
            for layout_item in layout_item_group
        ]
        for carrier, layout_item_group in groupby(
            loaded_layout_items,
            lambda x: x.deck_location.carrier_config.carrier,
        )
    ]
    # Now organize the items by carrier.
