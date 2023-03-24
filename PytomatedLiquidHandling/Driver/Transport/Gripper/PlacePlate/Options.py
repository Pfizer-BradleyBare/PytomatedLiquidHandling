from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        PlateSequence: str,
    ):

        self.PlateSequence: str = PlateSequence

        self.EjectTool: int = 0

        self.XSpeed: int = 4
        self.ZSpeed: float = 128.7
        self.PressOnDistance: float = 1
        self.CheckPlateExists: int = 0
