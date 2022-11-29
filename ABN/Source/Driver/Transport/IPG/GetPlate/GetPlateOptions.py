from .....Tools.AbstractClasses import ObjectABC


class GetPlateOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        PlateSequence: str,
        GripWidth: float,
        OpenWidth: float,
    ):

        self.Name: str = Name

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

    def GetName(self) -> str:
        return self.Name
