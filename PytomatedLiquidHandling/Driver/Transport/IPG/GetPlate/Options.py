from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        PlateSequence: str,
        GripWidth: float,
        OpenWidth: float,
    ):

        self.PlateSequence: str = PlateSequence

        self.GripHeight: float = 3
        self.GripMode: int = 0
        self.GripWidth: float = GripWidth
        self.OpenWidth: float = OpenWidth

        self.Movement: int = 0

        # Only matters if movement is 1
        self.RetractDistance: float = 0
        self.LiftupHeight: float = 0
        self.LabwareOrientation: int = 1

        self.GripForce: int = 5
        self.Tolerance: float = 2
        self.InverseGrip: int = 0
        self.CollisionControl: int = 1
