from __future__ import annotations

from plh.api.tools.loaded_labware import LoadedLabware
from plh.implementation import carrier_loader


def end(
    *args: tuple[LoadedLabware, None | LoadedLabware],
) -> None:
    """Will move the deck locations back into the deck using the associated carrier_mover."""
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

        loader.load(list(carriers)[0])
