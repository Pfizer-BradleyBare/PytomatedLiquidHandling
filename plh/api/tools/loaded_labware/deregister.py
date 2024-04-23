from __future__ import annotations

from .loaded_labware import LoadedLabware, loaded_labware_tracker


def deregister(loaded_labware: LoadedLabware) -> None:
    """Utility method to remove a loaded labware registration."""
    if loaded_labware.layout_item not in loaded_labware_tracker:
        raise RuntimeError("Layout item is not tracked. Critical error.")

    del loaded_labware_tracker[loaded_labware.layout_item]
