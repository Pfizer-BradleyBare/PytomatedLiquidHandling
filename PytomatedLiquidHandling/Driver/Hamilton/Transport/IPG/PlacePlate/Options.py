from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedOptionsABC


class AdvancedOptions(AdvancedOptionsABC):
    def __init__(
        self,
        *,
        CustomErrorHandling: bool | None = None,
        Movement: int | None = None,
        RetractDistance: float | None = None,
        LiftupHeight: float | None = None,
        LabwareOrientation: int | None = None,
        CollisionControl: int | None = None,
    ):
        AdvancedOptionsABC.__init__(self, CustomErrorHandling)
        self.Movement: int | None = Movement

        # Only matters if movement is 1
        self.RetractDistance: float | None = RetractDistance
        self.LiftupHeight: float | None = LiftupHeight
        self.LabwareOrientation: int | None = LabwareOrientation

        self.CollisionControl: int | None = CollisionControl


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        PlateSequence: str,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.PlateSequence: str = PlateSequence

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(
            CustomErrorHandling=False,
            Movement=0,
            RetractDistance=0,
            LiftupHeight=0,
            LabwareOrientation=1,
            CollisionControl=1,
        )
        # These are the default advanced values

        self.AdvancedOptionsInstance.__dict__.update(
            {k: v for k, v in vars(AdvancedOptionsInstance) if v is not None}
        )
        # This is used to update the values from the user if the user decided to change any advanced settings
