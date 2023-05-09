from ......Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        GripperSequence: str,
        PlateSequence: str,
        GripWidth: float,
        OpenWidth: float,
        CustomErrorHandling: bool = False,
        GripHeight: float = 3,
        GripForce: int = 4,
        GripSpeed: float = 277.8,
        ZSpeed: float = 128.7,
        CheckPlateExists: int = 0,
    ):
        self.PlateSequence: str = PlateSequence
        self.GripperSequence: str = GripperSequence

        self.GripWidth: float = GripWidth
        self.OpenWidth: float = OpenWidth

        self.GripHeight: float = GripHeight
        self.GripForce: int = GripForce
        self.GripSpeed: float = GripSpeed
        self.ZSpeed: float = ZSpeed
        self.CheckPlateExists: int = CheckPlateExists
