from __future__ import annotations

from plh.api.tools import loaded_labware


def prepare(
    *args: tuple[loaded_labware.LoadedLabware, None | loaded_labware.LoadedLabware]
) -> None:
    """Prepares the LoadedLabware returned from ```group``` for loading or unloading.
    If the tuple contains None then the loading locations will be emptied.
    If the tuple contains a LoadedLabware then the LoadedLabware will be moved to the position for unloading, swapping, or container addition.
    """
    ...
