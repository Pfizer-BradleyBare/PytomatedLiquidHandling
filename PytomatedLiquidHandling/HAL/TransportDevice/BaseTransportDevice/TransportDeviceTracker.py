from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from .TransportDevice import TransportDevice
from .Interface import TransportOptions


class TransportDeviceTracker(UniqueObjectTrackerABC[TransportDevice]):
    pass

    def Transport(self, OptionsTrackerInstance: TransportOptions.OptionsTracker):
        ...
