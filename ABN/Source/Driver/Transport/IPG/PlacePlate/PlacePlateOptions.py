from .....Tools.AbstractClasses import ObjectABC


class PlacePlateOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        PlateSequence: str,
    ):

        self.Name: str = Name

        self.PlateSequence: str = PlateSequence

        # Only matters if movement is 1
        self.RetractDistance: float = 0
        self.LiftupHeight: float = 0
        self.LabwareOrientation: int = 1

        self.CollisionControl: int = 1

    def GetName(self) -> str:
        return self.Name
