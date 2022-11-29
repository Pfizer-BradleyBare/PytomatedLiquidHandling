from .....Tools.AbstractClasses import ObjectABC


class PlacePlateOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        PlateSequence: str,
    ):

        self.Name: str = Name

        self.PlateSequence: str = PlateSequence

        self.EjectTool: int = 0

        self.XSpeed: int = 4
        self.ZSpeed: float = 128.7
        self.PressOnDistance: float = 1
        self.CheckPlateExists: int = 0

    def GetName(self) -> str:
        return self.Name
