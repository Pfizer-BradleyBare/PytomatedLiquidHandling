from abc import ABC


class AdvancedMultiOptionsABC(ABC):
    ...


class AdvancedMultiOptionsTrackerABC(ABC):
    def __init__(self, CustomErrorHandling: bool | None):
        self.CustomErrorHandling: bool | None = CustomErrorHandling
