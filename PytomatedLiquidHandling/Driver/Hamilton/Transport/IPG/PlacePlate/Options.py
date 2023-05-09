from ......Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        PlateSequence: str,
        Movement: int = 0,
        RetractDistance: float = 0,
        LiftupHeight: float = 0,
        LabwareOrientation: int = 1,
        CollisionControl: int = 1,
    ):
        self.PlateSequence: str = PlateSequence

        self.Movement: int = Movement

        # Only matters if movement is 1
        self.RetractDistance: float = RetractDistance
        self.LiftupHeight: float = LiftupHeight
        self.LabwareOrientation: int = LabwareOrientation

        self.CollisionControl: int = CollisionControl
