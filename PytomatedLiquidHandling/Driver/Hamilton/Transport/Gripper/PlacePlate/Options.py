from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedOptionsWrapper, AdvancedSingleOptionsABC


class AdvancedOptions(AdvancedSingleOptionsABC):
    @AdvancedOptionsWrapper
    def __init__(
        self,
        *,
        CustomErrorHandling: bool = False,
        EjectTool: int = 0,
        XSpeed: int = 4,
        ZSpeed: float = 128.7,
        PressOnDistance: float = 1,
        CheckPlateExists: int = 0,
    ):
        AdvancedSingleOptionsABC.__init__(self, CustomErrorHandling)
        self.EjectTool: int = EjectTool
        self.XSpeed: int = XSpeed
        self.ZSpeed: float = ZSpeed
        self.PressOnDistance: float = PressOnDistance
        self.CheckPlateExists: int = CheckPlateExists


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        PlateSequence: str,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.PlateSequence: str = PlateSequence

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptionsInstance
