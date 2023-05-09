from .....Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .AdvancedMultiOptionsABC import AdvancedMultiOptionsABC


class AdvancedMultiOptionsTrackerABC(
    NonUniqueObjectTrackerABC[AdvancedMultiOptionsABC]
):
    def __init__(self, CustomErrorHandling: bool):
        self.CustomErrorHandling: bool = CustomErrorHandling
        NonUniqueObjectTrackerABC.__init__(self)
