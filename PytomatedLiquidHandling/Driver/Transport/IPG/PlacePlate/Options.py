from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        PlateSequence: str,
    ):

        self.PlateSequence: str = PlateSequence

        self.Movement: int = 0

        # Only matters if movement is 1
        self.RetractDistance: float = 0
        self.LiftupHeight: float = 0
        self.LabwareOrientation: int = 1

        self.CollisionControl: int = 1
