from ....Tools.AbstractClasses import ObjectABC


class StartTimerOptions(ObjectABC):
    def __init__(self, Name: str, WaitTime: float):

        self.Name: str = Name

        self.WaitTime: float = WaitTime

    def GetName(self) -> str:
        return self.Name
