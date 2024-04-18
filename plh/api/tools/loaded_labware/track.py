from __future__ import annotations

from .loaded_labware import LoadedLabware, loaded_labware_tracker


def track(loaded_labware: LoadedLabware) -> None:
    """Utility method to register a loaded labware."""
    if loaded_labware.layout_item in loaded_labware_tracker:
        raise RuntimeError("Layout item already taken. Critical error.")

    loaded_labware_tracker[loaded_labware.layout_item] = loaded_labware
