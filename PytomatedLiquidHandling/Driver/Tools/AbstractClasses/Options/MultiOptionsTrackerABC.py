from .....Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .MultiOptionsABC import MultiOptionsABC


class MultiOptionsTrackerABC(NonUniqueObjectTrackerABC[MultiOptionsABC]):
    def __init__(self, CustomErrorHandling: bool):
        self.CustomErrorHandling: bool = CustomErrorHandling
        NonUniqueObjectTrackerABC.__init__(self)
