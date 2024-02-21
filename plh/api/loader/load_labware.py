from __future__ import annotations

from dataclasses import dataclass

from plh.api import container
from plh.hal import carrier_loader, labware, layout_item


@dataclass
class LoadedLabware:
    """Labware they is loaded on the deck or is in the process of being loaded on deck."""

    labware: labware.LabwareBase
    """The labware type."""

    layout_item: layout_item.LayoutItemBase
    """Where it is or will be on deck."""

    well_assignments: tuple[container.Well, ...]
    """Wells that have been assigned to the container."""


def group(labwares: list[labware.LabwareBase]) -> list[list[LoadedLabware]]:
    """Takes a list of labware and groups it by carrier for loading."""
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

    loadable_labware = [layout_item.labware for layout_item in loadable_layout_items]

    available_labware = dict(
        sorted(
            {
                labware: loadable_labware.count(labware)
                for labware in set(loadable_labware)
            }.items(),
            key=lambda x: x[1],
        ),
    )
    # get number of available labware positions

    required_labware = dict(
        sorted(
            {labware: labwares.count(labware) for labware in set(labwares)}.items(),
            key=lambda x: x[1],
        ),
    )
    # get number of each labware we need to load.

    exceptions = [
        RuntimeError("")
        for labware, labware_number in required_labware.items()
        if labware_number > available_labware[labware]
    ]

    if len(exceptions) != 0:
        raise ExceptionGroup("Not enough labware positions available", exceptions)
