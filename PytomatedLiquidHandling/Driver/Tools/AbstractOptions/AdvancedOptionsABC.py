from abc import ABC


class AdvancedOptionsABC:
    def __init__(self, CustomErrorHandling: bool | None):
        self.CustomErrorHandling: bool | None = CustomErrorHandling
