from ....AbstractClasses import TrackerABC
from ....AbstractClasses import ObjectABC
from ...Workbook.Block import Block
from ...Workbook.Block import BlockTracker


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


class Container(ObjectABC):
    def __init__(self, Name: str, Filter: str):

        self.Name: str = Name

        # Block Instances: These are the blocks that have used this container. Either for aspirate or dispense.
        self.AspirateBlockTrackerInstance: BlockTracker = BlockTracker()
        self.DispenseBlockTrackerInstances: BlockTracker = BlockTracker()

        # This is used for automated deck loading. We have to restrict the choices based on the filter
        self.Filter: str = Filter

        # What solutions and volume is in each well
        self.WellTrackerInstance: WellTracker = WellTracker()

        # What wells have been overaspirated
        self.WellOverAspirateTrackerInstance: WellTracker = WellTracker()

        self.MaxWellVolume: float = 0

    def GetName(self) -> str:
        return self.Name

    def GetAspirateBlocks(self) -> list[Block]:
        return self.AspirateBlockInstances

    def GetDispenseBlocks(self) -> list[Block]:
        return self.DispenseBlockInstances

    def GetFilter(self) -> str:
        return self.Filter

    def GetWellTracker(self) -> WellTracker:
        return self.WellTrackerInstance

    def GetWellOverAspirateTracker(self) -> WellTracker:
        return self.WellOverAspirateTrackerInstance

    def GetMaxVolume(self) -> float:
        return self.MaxWellVolume
