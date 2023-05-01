from ......Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .....Tools.AbstractOptions import AdvancedMultiOptionsTrackerABC
from .Options import Options


class AdvancedOptionsTracker(AdvancedMultiOptionsTrackerABC):
    def __init__(self, *, CustomErrorHandling: bool | None = None):
        AdvancedMultiOptionsTrackerABC.__init__(self, CustomErrorHandling)


class OptionsTracker(NonUniqueObjectTrackerABC[Options]):
    def __init__(
        self,
        *,
        AdvancedOptionsTrackerInstance: AdvancedOptionsTracker = AdvancedOptionsTracker()
    ):
        NonUniqueObjectTrackerABC.__init__(self)

        self.AdvancedOptionsTrackerInstance: AdvancedOptionsTracker = (
            AdvancedOptionsTracker(CustomErrorHandling=False)
        )
        # These are the default advanced values

        self.AdvancedOptionsTrackerInstance.__dict__.update(
            {k: v for k, v in vars(AdvancedOptionsTrackerInstance) if v is not None}
        )
        # This is used to update the values from the user if the user decided to change any advanced settings
