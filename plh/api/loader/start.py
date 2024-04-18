from __future__ import annotations

from plh.api.tools import loaded_labware
from plh.hal import carrier_loader


def start(
    *args: tuple[loaded_labware.LoadedLabware, None | loaded_labware.LoadedLabware],
) -> None:
    """Will move the deck locations out to the user using the associated carrier_mover."""
    carriers = {
        item.layout_item.deck_location.carrier_config.carrier for item, meta in args
    }

    if len(carriers) != 1:
        raise RuntimeError(
            "You can only load 1 carrier at a time. The list your provided relies on multiple carriers...",
        )
    # are all carriers the same?

    for loader in carrier_loader.devices.values():
        try:
            loader.assert_supported_carriers(*list(carriers))
        except ExceptionGroup:
            ...
            # continue
        # Find our correct carrier loader

        loader.unload(list(carriers)[0])
