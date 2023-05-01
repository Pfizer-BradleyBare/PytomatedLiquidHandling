from abc import ABC


class AdvancedSingleOptionsABC(ABC):
    def __init__(self, CustomErrorHandling: bool | None):
        self.CustomErrorHandling: bool | None = CustomErrorHandling
