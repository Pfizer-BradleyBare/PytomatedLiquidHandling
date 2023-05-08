from ..AdvancedOptions import AdvancedSingleOptionsABC


class SingleOptionsABC:
    def __init__(self, AdvancedOptionsInstance: AdvancedSingleOptionsABC):
        self.AdvancedOptionsInstance: AdvancedSingleOptionsABC = AdvancedOptionsInstance
