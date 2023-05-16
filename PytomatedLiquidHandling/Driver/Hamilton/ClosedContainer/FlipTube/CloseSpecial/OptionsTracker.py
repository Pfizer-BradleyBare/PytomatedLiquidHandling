from .....Tools.AbstractClasses import OptionsTrackerABC

from .Options import Options


class OptionsTracker(OptionsTrackerABC[Options]):
    def __init__(
        self,
        *,
        ToolSequence: str,
    ):
        OptionsTrackerABC.__init__(self)

        self.ToolSequence: str = ToolSequence
