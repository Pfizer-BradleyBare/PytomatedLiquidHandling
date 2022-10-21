from ..Container import Container, ContainerTypes
from .....AbstractClasses.Tracker import TrackerABC


class WellSolution:
    def __init__(self, Name: str, Volume: float):
        self.Name: str = Name
        self.Volume: float = Volume

    def GetName(self) -> str:
        return self.Name

    def GetVolume(self) -> float:
        return self.Volume


class WellSolutionTracker(TrackerABC):
    def __init__(self, WellNumber: int):
        self.WellNumber: int = WellNumber
        self.Collection: dict[str, WellSolution] = dict()

    def GetWellNumber(self) -> int:
        return self.WellNumber

    def LoadManual(self, WellSolutionInstance: WellSolution):
        Name = WellSolutionInstance.GetName()

        if str(Name) in self.Collection:
            raise Exception("Solution Already Exists")

        self.Collection[Name] = WellSolutionInstance

    def GetObjectsAsList(self) -> list[WellSolution]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[str, WellSolution]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> WellSolution:
        return self.Collection[Name]


class WellTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, WellSolutionTracker] = dict()

    def LoadManual(self, WellSolutionTrackerInstance: WellSolutionTracker):
        Name = WellSolutionTrackerInstance.GetWellNumber()

        if str(Name) in self.Collection:
            raise Exception("Well Already Exists")

        self.Collection[Name] = WellSolutionTrackerInstance

    def GetObjectsAsList(self) -> list[WellSolutionTracker]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[str, WellSolutionTracker]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> WellSolutionTracker:
        return self.Collection[Name]


class PlateContainer(Container):
    def __init__(self, Name: str, Filter: str):
        Container.__init__(self, Name, ContainerTypes.Plate)

        # This is used for automated deck loading. We have to restrict the choices based on the filter
        self.Filter: str = Filter

        self.WellTrackerInstance: WellTracker = WellTracker()
        self.MinVolume: float = 0
        self.MaxVolume: float = 0

    def GetFilter(self) -> str:
        return self.Filter

    def GetWellTrackerInstance(self) -> WellTracker:
        return self.WellTrackerInstance

    def GetMinVolume(self) -> float:
        return self.MinVolume

    def GetMaxVolume(self) -> float:
        return self.MaxVolume
