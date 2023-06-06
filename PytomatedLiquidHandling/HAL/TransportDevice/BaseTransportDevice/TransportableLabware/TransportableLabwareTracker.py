from .....Tools.AbstractClasses import UniqueObjectTrackerABC
from .TransportableLabware import TransportableLabware
from dataclasses import dataclass


@dataclass
class TransportableLabwareTracker(UniqueObjectTrackerABC[TransportableLabware]):
    ...
