from .....Tools.AbstractClasses import OptionsTrackerABC
from .Options import Options


class OptionsTracker(OptionsTrackerABC[Options]):
    def __init__(
        self,
        *,
        Sequence: str,
    ):
        OptionsTrackerABC.__init__(self)

        self.Sequence: str = Sequence
