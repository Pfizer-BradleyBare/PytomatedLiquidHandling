from __future__ import annotations

from plh.api.tools import LoadedLabware


def prepare(
    *args: tuple[LoadedLabware, None | LoadedLabware],
) -> None:
    """Prepares the LoadedLabware returned from ```group``` for loading or unloading.
    If the tuple contains None then the loading locations will be emptied.
    If the tuple contains a LoadedLabware then the LoadedLabware will be moved to the position for unloading, swapping, or container addition.
    """
    ...
