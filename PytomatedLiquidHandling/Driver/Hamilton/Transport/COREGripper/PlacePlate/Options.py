from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        PlateSequence: str,
        EjectTool: int = 0,
        XSpeed: int = 4,
        ZSpeed: float = 128.7,
        PressOnDistance: float = 1,
        CheckPlateExists: int = 0,
    ):
        self.PlateSequence: str = PlateSequence

        self.EjectTool: int = EjectTool
        self.XSpeed: int = XSpeed
        self.ZSpeed: float = ZSpeed
        self.PressOnDistance: float = PressOnDistance
        self.CheckPlateExists: int = CheckPlateExists