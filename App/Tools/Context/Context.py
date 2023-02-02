from ....Tools.AbstractClasses import ObjectABC
from .States.ContextStates import ContextStates
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

        class ContextState:
            def __init__(self):
                self.State: ContextStates = ContextStates.Running
                self.Reason: str = "Context is running normally."

        self.ContextStateInstance: ContextState = ContextState()

        self.AspirateWellSequenceTrackerInstance: WellSequenceTracker = (
            AspirateWellSequenceTrackerInstance
        )
        self.DispenseWellSequenceTrackerInstance: WellSequenceTracker = (
            DispenseWellSequenceTrackerInstance
        )
        self.WellFactorsTrackerInstance: WellFactorTracker = WellFactorsTrackerInstance

    def GetName(self) -> str:
        return self.Name

    def UpdateContextState(self, NewState: ContextStates, Reason: str):
        self.ContextStateInstance.State = NewState
        self.ContextStateInstance.Reason = Reason

    def GetAspirateWellSequenceTracker(self) -> WellSequenceTracker:
        return self.AspirateWellSequenceTrackerInstance

    def GetDispenseWellSequenceTracker(self) -> WellSequenceTracker:
        return self.DispenseWellSequenceTrackerInstance

    def GetWellFactorTracker(self) -> WellFactorTracker:
        return self.WellFactorsTrackerInstance
