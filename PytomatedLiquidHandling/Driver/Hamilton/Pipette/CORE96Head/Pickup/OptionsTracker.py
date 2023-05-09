from ......Tools.AbstractClasses import NonUniqueObjectTrackerABC

from .Options import Options


class OptionsTracker(NonUniqueObjectTrackerABC[Options]):
    def __init__(
        self,
        *,
        Sequence: str,
    ):
        NonUniqueObjectTrackerABC.__init__(self)

        self.Sequence: str = Sequence
