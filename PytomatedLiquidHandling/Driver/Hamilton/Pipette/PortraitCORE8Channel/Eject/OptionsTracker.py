from ......Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .....Tools.AbstractOptions import (
    AdvancedMultiOptionsTrackerABC,
    AdvancedOptionsWrapper,
)
from .Options import Options


class AdvancedOptionsTracker(AdvancedMultiOptionsTrackerABC):
    @AdvancedOptionsWrapper
    def __init__(self, *, CustomErrorHandling: bool = False):
        AdvancedMultiOptionsTrackerABC.__init__(self, CustomErrorHandling)


class OptionsTracker(NonUniqueObjectTrackerABC[Options]):
    def __init__(
        self,
        *,
        AdvancedOptionsTrackerInstance: AdvancedOptionsTracker = AdvancedOptionsTracker()
    ):
        NonUniqueObjectTrackerABC.__init__(self)

        self.AdvancedOptionsTrackerInstance: AdvancedOptionsTracker = (
            AdvancedOptionsTrackerInstance
        )