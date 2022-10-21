from ....AbstractClasses import ObjectABC, TrackerABC


class WellFactors(ObjectABC):
    def __init__(self):
        pass

    def GetName(self) -> str:
        return self.Name


class WellFactorsTracker(TrackerABC, ObjectABC):
    def __init__(self, WellNumber: int):
        self.WellNumber: int = WellNumber
        self.Collection: dict[str, WellFactors] = dict()

    def GetName(self) -> str:
        return str(self.WellNumber)

    def LoadManual(self, WellSolutionInstance: WellFactors):
        Name = WellSolutionInstance.GetName()

        if str(Name) in self.Collection:
            raise Exception("Solution Already Exists")

        self.Collection[Name] = WellSolutionInstance

    def GetObjectsAsList(self) -> list[WellFactors]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[str, WellFactors]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> WellFactors:
        return self.Collection[Name]


class WellSequences(ObjectABC):
    def __init__(self):
        pass

    def GetName(self) -> str:
        return self.Name


class WellSequencesTracker(TrackerABC, ObjectABC):
    def __init__(self, WellNumber: int):
        self.WellNumber: int = WellNumber
        self.Collection: dict[str, WellSequences] = dict()

    def GetName(self) -> str:
        return str(self.WellNumber)

    def LoadManual(self, WellSolutionInstance: WellSequences):
        Name = WellSolutionInstance.GetName()

        if str(Name) in self.Collection:
            raise Exception("Solution Already Exists")

        self.Collection[Name] = WellSolutionInstance

    def GetObjectsAsList(self) -> list[WellSequences]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[str, WellSequences]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> WellSequences:
        return self.Collection[Name]


class Context(ObjectABC):
    def __init__(
        self,
        Name: str,
        AspirateWellSequencesTrackerInstance: WellSequencesTracker,
        DispenseWellSequencesTrackerInstance: WellSequencesTracker,
        AspirateWellFactorsTrackerInstance: WellFactorsTracker,
        DispenseWellFactorsTrackerInstance: WellFactorsTracker,
    ):
        self.Name: str = Name
        self.AspirateWellSequencesTrackerInstance: WellSequencesTracker = (
            AspirateWellSequencesTrackerInstance
        )
        self.DispenseWellSequencesTrackerInstance: WellSequencesTracker = (
            DispenseWellSequencesTrackerInstance
        )
        self.AspirateWellFactorsTrackerInstance: WellFactorsTracker = (
            AspirateWellFactorsTrackerInstance
        )
        self.DispenseWellFactorsTrackerInstance: WellFactorsTracker = (
            DispenseWellFactorsTrackerInstance
        )

    def GetName(self) -> str:
        return self.Name

    def GetAspirateWellSequencesTracker(self) -> WellSequencesTracker:
        return self.AspirateWellSequencesTrackerInstance

    def GetDispenseWellSequencesTracker(self) -> WellSequencesTracker:
        return self.DispenseWellSequencesTrackerInstance

    def GetAspirateWellFactorsTracker(self) -> WellFactorsTracker:
        return self.AspirateWellFactorsTrackerInstance

    def GetDispenseWellFactorsTracker(self) -> WellFactorsTracker:
        return self.DispenseWellFactorsTrackerInstance


class ContextTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Context] = dict()

    def LoadManual(self, ContextInstance: Context):
        Name = ContextInstance.GetName()

        if str(Name) in self.Collection:
            raise Exception("Context Already Exists")

        self.Collection[Name] = ContextInstance

    def GetObjectsAsList(self) -> list[Context]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[Context]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Context:
        return self.Collection[Name]
