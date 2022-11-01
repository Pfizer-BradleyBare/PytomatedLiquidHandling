from ....AbstractClasses import ObjectABC
from .WellFactor.WellFactorTracker import WellFactorTracker
from .WellSequence.WellSequenceTracker import WellSequenceTracker


class Context(ObjectABC):
    def __init__(
        self,
        Name: str,
        AspirateWellSequenceTrackerInstance: WellSequenceTracker,
        DispenseWellSequenceTrackerInstance: WellSequenceTracker,
        WellFactorsTrackerInstance: WellFactorTracker,
    ):
        self.Name: str = Name
        self.AspirateWellSequenceTrackerInstance: WellSequenceTracker = (
            AspirateWellSequenceTrackerInstance
        )
        self.DispenseWellSequenceTrackerInstance: WellSequenceTracker = (
            DispenseWellSequenceTrackerInstance
        )
        self.WellFactorsTrackerInstance: WellFactorTracker = WellFactorsTrackerInstance

    def GetName(self) -> str:
        return self.Name

    def GetAspirateWellSequenceTracker(self) -> WellSequenceTracker:
        return self.AspirateWellSequenceTrackerInstance

    def GetDispenseWellSequenceTracker(self) -> WellSequenceTracker:
        return self.DispenseWellSequenceTrackerInstance

    def GetWellFactorTracker(self) -> WellFactorTracker:
        return self.WellFactorsTrackerInstance
