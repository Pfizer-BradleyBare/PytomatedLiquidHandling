from __future__ import annotations

from plh.api.tools import loaded_labware


def load(*args: loaded_labware.LoadedLabware) -> None:
    """Will add the labware in the labware tracker. This officially makes the API layer aware that the labware is now on the deck."""
    for item in args:
        if item.layout_item in loaded_labware.loaded_labware_tracker:
            raise RuntimeError("Layout item already taken. Critical error.")

        loaded_labware.loaded_labware_tracker[item.layout_item] = item
