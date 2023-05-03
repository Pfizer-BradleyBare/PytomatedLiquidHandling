from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedOptionsWrapper, AdvancedSingleOptionsABC


class AdvancedOptions(AdvancedSingleOptionsABC):
    @AdvancedOptionsWrapper
    def __init__(self, *, CustomErrorHandling: bool = False):
        AdvancedSingleOptionsABC.__init__(self, CustomErrorHandling)


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        ComPort: str,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions()
    ):
        self.ComPort: str = ComPort

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptionsInstance
