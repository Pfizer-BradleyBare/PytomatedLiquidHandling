from .Method import Method
from ...AbstractClasses import TrackerABC


class MethodTracker(TrackerABC):
    def __init__(self):
        self.Methods: dict[str, Method] = dict()

    def LoadManual(self, MethodInstance: Method):
        Name = MethodInstance.GetName()

        if Name in self.Collection:
            raise Exception("Method Already Exists")

        self.Collection[Name] = MethodInstance

    def GetObjectsAsList(self) -> list[Method]:
        return self.Blocks

    def GetObjectsAsDictionary(self) -> dict[str, Method]:
        return {
            Block.GetTitle() + " " + str(Block.GetCoordinates()): Block
            for Block in self.Blocks
        }

    def GetObjectByName(self, Name: str):
        return self.Methods[Name]
