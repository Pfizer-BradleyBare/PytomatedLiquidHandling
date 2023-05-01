from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedMultiOptionsABC


class AdvancedOptions(AdvancedMultiOptionsABC):
    def __init__(
        self,
        *,
        GripHeight: float | None = None,
        GripMode: int | None = None,
        Movement: int | None = None,
        RetractDistance: float | None = None,
        LiftupHeight: float | None = None,
        LabwareOrientation: int | None = None,
        GripForce: int | None = None,
        Tolerance: float | None = None,
        InverseGrip: int | None = None,
        CollisionControl: int | None = None,
    ):
        AdvancedMultiOptionsABC.__init__(self)
        self.GripHeight: float | None = GripHeight
        self.GripMode: int | None = GripMode

        self.Movement: int | None = Movement

        # Only matters if movement is 1
        self.RetractDistance: float | None = RetractDistance
        self.LiftupHeight: float | None = LiftupHeight
        self.LabwareOrientation: int | None = LabwareOrientation

        self.GripForce: int | None = GripForce
        self.Tolerance: float | None = Tolerance
        self.InverseGrip: int | None = InverseGrip
        self.CollisionControl: int | None = CollisionControl


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

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(
            GripHeight=3,
            GripMode=0,
            Movement=0,
            RetractDistance=0,
            LiftupHeight=0,
            LabwareOrientation=1,
            GripForce=4,
            Tolerance=2,
            InverseGrip=0,
            CollisionControl=1,
        )
        # These are the default advanced values

        self.AdvancedOptionsInstance.__dict__.update(
            {k: v for k, v in vars(AdvancedOptionsInstance) if v is not None}
        )
        # This is used to update the values from the user if the user decided to change any advanced settings
