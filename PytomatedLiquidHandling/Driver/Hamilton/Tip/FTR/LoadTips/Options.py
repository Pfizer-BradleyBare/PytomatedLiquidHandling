from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedOptionsWrapper, AdvancedSingleOptionsABC


class AdvancedOptions(AdvancedSingleOptionsABC):
    @AdvancedOptionsWrapper
    def __init__(self, *, CustomErrorHandling: bool = False, MinimumTips: int = 0):
        AdvancedSingleOptionsABC.__init__(self, CustomErrorHandling)
        self.MinimumTips: int = MinimumTips


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        TipSequence: str,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.TipSequence: str = TipSequence

        self.LoadingText: str = "Load FTR Tips"

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptionsInstance
