from ......Tools.AbstractClasses import NonUniqueObjectTrackerABC

from .Options import Options


class OptionsTracker(NonUniqueObjectTrackerABC[Options]):
    def __init__(self):
        NonUniqueObjectTrackerABC.__init__(self)
