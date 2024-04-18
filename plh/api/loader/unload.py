from __future__ import annotations

from plh.api.tools import LoadedLabware, loaded_labware_tracker


def unload(*args: LoadedLabware) -> None:
    """Will remove the labware from the labware tracker. The API layer now assumes that this labware is no longer on the deck."""
    for item in args:
        if item.layout_item not in loaded_labware_tracker:
            raise RuntimeError("Layout item is not tracked. Critical error.")

        del loaded_labware_tracker[item.layout_item]
