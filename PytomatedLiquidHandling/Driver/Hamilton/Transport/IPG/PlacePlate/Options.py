from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedOptionsWrapper, AdvancedSingleOptionsABC


class AdvancedOptions(AdvancedSingleOptionsABC):
    @AdvancedOptionsWrapper
    def __init__(
        self,
        *,
        CustomErrorHandling: bool = False,
        Movement: int = 0,
        RetractDistance: float = 0,
        LiftupHeight: float = 0,
        LabwareOrientation: int = 1,
        CollisionControl: int = 1,
    ):
        AdvancedSingleOptionsABC.__init__(self, CustomErrorHandling)
        self.Movement: int = Movement

        # Only matters if movement is 1
        self.RetractDistance: float = RetractDistance
        self.LiftupHeight: float = LiftupHeight
        self.LabwareOrientation: int = LabwareOrientation

        self.CollisionControl: int = CollisionControl


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        PlateSequence: str,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.PlateSequence: str = PlateSequence

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptionsInstance
