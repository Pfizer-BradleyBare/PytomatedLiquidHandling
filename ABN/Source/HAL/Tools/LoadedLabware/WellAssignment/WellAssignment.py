from .....Tools.AbstractClasses import ObjectABC


class WellAssignment(ObjectABC):
    def __init__(
        self,
        MethodName: str,
        SampleNumber: int,
        SampleDescription: str,
        WellNumber: int,
    ):
        self.Name: str = (
            MethodName + " - " + str(SampleNumber) + ":" + SampleDescription
        )
        self.WellNumber: int = WellNumber

    def GetName(self) -> str:
        return self.Name

    def GetWellNumber(self) -> int:
        return self.WellNumber
