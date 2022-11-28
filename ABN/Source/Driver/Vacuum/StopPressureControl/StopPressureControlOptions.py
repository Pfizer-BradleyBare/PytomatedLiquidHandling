from ....Tools.AbstractClasses import ObjectABC


class StopPressureControlOptions(ObjectABC):
    def __init__(self, Name: str, HandleID: int):

        self.Name: str = Name

        self.HandleID: int = HandleID

    def GetName(self) -> str:
        return self.Name
