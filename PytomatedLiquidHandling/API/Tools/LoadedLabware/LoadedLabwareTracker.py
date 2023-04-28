from typing import Self

from ....Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .LoadedLabware import LoadedLabware


class LoadedLabwareTracker(NonUniqueObjectTrackerABC[LoadedLabware]):
    ...
