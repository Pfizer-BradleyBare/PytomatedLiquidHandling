from ....AbstractClasses import ObjectABC
from .WellFactor.WellFactorTracker import WellFactorTracker
from .WellSequences.WellSequencesTracker import WellSequencesTracker


class Context(ObjectABC):
    def __init__(
        self,
        Name: str,
        AspirateWellSequencesTrackerInstance: WellSequencesTracker,
        DispenseWellSequencesTrackerInstance: WellSequencesTracker,
        WellFactorsTrackerInstance: WellFactorTracker,
    ):
        self.Name: str = Name
        self.AspirateWellSequencesTrackerInstance: WellSequencesTracker = (
            AspirateWellSequencesTrackerInstance
        )
        self.DispenseWellSequencesTrackerInstance: WellSequencesTracker = (
            DispenseWellSequencesTrackerInstance
        )
        self.WellFactorsTrackerInstance: WellFactorTracker = WellFactorsTrackerInstance

    def GetName(self) -> str:
        return self.Name

    def GetAspirateWellSequencesTracker(self) -> WellSequencesTracker:
        return self.AspirateWellSequencesTrackerInstance

    def GetDispenseWellSequencesTracker(self) -> WellSequencesTracker:
        return self.DispenseWellSequencesTrackerInstance

    def GetWellFactorTracker(self) -> WellFactorTracker:
        return self.WellFactorsTrackerInstance
