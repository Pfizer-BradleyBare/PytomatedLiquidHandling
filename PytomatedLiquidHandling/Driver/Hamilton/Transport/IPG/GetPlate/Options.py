from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedOptionsWrapper, AdvancedSingleOptionsABC


class AdvancedOptions(AdvancedSingleOptionsABC):
    @AdvancedOptionsWrapper
    def __init__(
        self,
        *,
        CustomErrorHandling: bool = False,
        GripHeight: float = 3,
        GripMode: int = 0,
        Movement: int = 0,
        RetractDistance: float = 0,
        LiftupHeight: float = 0,
        LabwareOrientation: int = 1,
        GripForce: int = 4,
        Tolerance: float = 2,
        InverseGrip: int = 0,
        CollisionControl: int = 1,
    ):
        AdvancedSingleOptionsABC.__init__(self, CustomErrorHandling)
        self.GripHeight: float = GripHeight
        self.GripMode: int = GripMode

        self.Movement: int = Movement

        # Only matters if movement is 1
        self.RetractDistance: float = RetractDistance
        self.LiftupHeight: float = LiftupHeight
        self.LabwareOrientation: int = LabwareOrientation

        self.GripForce: int = GripForce
        self.Tolerance: float = Tolerance
        self.InverseGrip: int = InverseGrip
        self.CollisionControl: int = CollisionControl


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        PlateSequence: str,
        GripWidth: float,
        OpenWidth: float,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.PlateSequence: str = PlateSequence

        self.GripWidth: float = GripWidth
        self.OpenWidth: float = OpenWidth

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptionsInstance
