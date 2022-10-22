from ....AbstractClasses import ObjectABC
from .WellFactor.WellFactorTracker import WellFactorTracker
from .WellSequences.WellSequencesTracker import WellSequencesTracker


class Context(ObjectABC):
    def __init__(
        self,
        Name: str,
        AspirateWellSequencesTrackerInstance: WellSequencesTracker,
        DispenseWellSequencesTrackerInstance: WellSequencesTracker,
        AspirateWellFactorsTrackerInstance: WellFactorTracker,
        DispenseWellFactorsTrackerInstance: WellFactorTracker,
    ):
        self.Name: str = Name
        self.AspirateWellSequencesTrackerInstance: WellSequencesTracker = (
            AspirateWellSequencesTrackerInstance
        )
        self.DispenseWellSequencesTrackerInstance: WellSequencesTracker = (
            DispenseWellSequencesTrackerInstance
        )
        self.AspirateWellFactorsTrackerInstance: WellFactorTracker = (
            AspirateWellFactorsTrackerInstance
        )
        self.DispenseWellFactorsTrackerInstance: WellFactorTracker = (
            DispenseWellFactorsTrackerInstance
        )

    def GetName(self) -> str:
        return self.Name

    def GetAspirateWellSequencesTracker(self) -> WellSequencesTracker:
        return self.AspirateWellSequencesTrackerInstance

    def GetDispenseWellSequencesTracker(self) -> WellSequencesTracker:
        return self.DispenseWellSequencesTrackerInstance

    def GetAspirateWellFactorTracker(self) -> WellFactorTracker:
        return self.AspirateWellFactorsTrackerInstance

    def GetDispenseWellFactorTracker(self) -> WellFactorTracker:
        return self.DispenseWellFactorsTrackerInstance
