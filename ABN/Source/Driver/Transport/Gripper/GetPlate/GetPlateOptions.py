from .....Tools.AbstractClasses import ObjectABC


class GetPlateOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        GripperSequence: str,
        PlateSequence: str,
        GripWidth: float,
        OpenWidth: float,
    ):

        self.Name: str = Name

        self.PlateSequence: str = PlateSequence
        self.GripperSequence: str = GripperSequence

        self.GripHeight: float = 3
        self.GripWidth: float = GripWidth
        self.OpenWidth: float = OpenWidth

        self.GripForce: int = 4
        self.GripSpeed: float = 277.8
        self.ZSpeed: float = 128.7
        self.CheckPlateExists: int = 0

    def GetName(self) -> str:
        return self.Name
