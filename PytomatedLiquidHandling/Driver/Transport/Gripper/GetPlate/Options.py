from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        GripperSequence: str,
        PlateSequence: str,
        GripWidth: float,
        OpenWidth: float,
    ):

        self.PlateSequence: str = PlateSequence
        self.GripperSequence: str = GripperSequence

        self.GripHeight: float = 3
        self.GripWidth: float = GripWidth
        self.OpenWidth: float = OpenWidth

        self.GripForce: int = 4
        self.GripSpeed: float = 277.8
        self.ZSpeed: float = 128.7
        self.CheckPlateExists: int = 0
