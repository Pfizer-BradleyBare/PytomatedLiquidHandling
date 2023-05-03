from .....Tools.AbstractClasses import NonUniqueObjectABC
from ....Tools.AbstractOptions import AdvancedOptionsWrapper, AdvancedSingleOptionsABC


class AdvancedOptions(AdvancedSingleOptionsABC):
    @AdvancedOptionsWrapper
    def __init__(self, *, CustomErrorHandling: bool = False):
        AdvancedSingleOptionsABC.__init__(self, CustomErrorHandling)


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        PumpID: int,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.PumpID: int = PumpID

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptionsInstance
