from ......Tools.AbstractClasses import NonUniqueObjectTrackerABC

from .Options import Options


class OptionsTracker(NonUniqueObjectTrackerABC[Options]):
    def __init__(
        self,
        *,
        ToolSequence: str,
    ):
        NonUniqueObjectTrackerABC.__init__(self)

        self.ToolSequence: str = ToolSequence
