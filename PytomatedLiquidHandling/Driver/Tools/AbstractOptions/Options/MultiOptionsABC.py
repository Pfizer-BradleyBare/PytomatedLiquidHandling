from ..AdvancedOptions import AdvancedMultiOptionsABC


class MultiOptionsABC:
    def __init__(self, AdvancedOptionsInstance: AdvancedMultiOptionsABC):
        self.AdvancedOptionsInstance: AdvancedMultiOptionsABC = AdvancedOptionsInstance
