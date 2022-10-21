from ....AbstractClasses import ObjectABC, TrackerABC


class WellFactors(ObjectABC):
    pass


class WellFactorsTracker(TrackerABC):
    pass


class WellSequences(ObjectABC):
    pass


class WellSequencesTracker(TrackerABC):
    pass


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
        raise NotImplementedError

    def GetAspirateWellSequencesTracker(self) -> WellSequencesTracker:
        return self.AspirateWellSequencesTrackerInstance

    def GetDispenseWellSequencesTracker(self) -> WellSequencesTracker:
        return self.DispenseWellSequencesTrackerInstance

    def GetAspirateWellFactorsTracker(self) -> WellFactorsTracker:
        return self.AspirateWellFactorsTrackerInstance

    def GetDispenseWellFactorsTracker(self) -> WellFactorsTracker:
        return self.DispenseWellFactorsTrackerInstance


class ContextTracker(TrackerABC):
    pass
