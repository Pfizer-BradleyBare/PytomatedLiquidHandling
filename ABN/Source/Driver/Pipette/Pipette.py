from ...AbstractClasses import DriverABC
from .Sequence.SequenceTracker import SequenceTracker
from ...HAL.Pipette import PipetteTracker
from ...HAL.Tools import DeckLoadingItemTracker
from ...API.Tools.Context import Context


class PipetteDriver(DriverABC):
    def __init__(
        self,
        SimulateState: bool,
        SequenceTrackerInstance: SequenceTracker,
        DeckLoadingItemTrackerInstance: DeckLoadingItemTracker,
        ContextInstance: Context,
        AspiratePipettingDeviceTrackerInstance: PipetteTracker,
        DispensePipettingDeviceTrackerInstance: PipetteTracker,
        # We have both aspirate and dispense pipetting devices because aspirate vs dispense liquid classes can be different.
    ):
        DriverABC.__init__(self, SimulateState)
        self.SequenceTrackerInstance: SequenceTracker = SequenceTrackerInstance
        self.DeckLoadingItemTrackerInstance: DeckLoadingItemTracker = (
            DeckLoadingItemTrackerInstance
        )
        self.ContextInstance: Context = ContextInstance
        self.AspiratePipettingDeviceTrackerInstance: PipetteTracker = (
            AspiratePipettingDeviceTrackerInstance
        )
        self.DispensePipettingDeviceTrackerInstance: PipetteTracker = (
            DispensePipettingDeviceTrackerInstance
        )

    def GetSequenceTracker(self) -> SequenceTracker:
        return self.SequenceTrackerInstance

    def GetDeckLoadingItemTracker(self) -> DeckLoadingItemTracker:
        return self.DeckLoadingItemTrackerInstance

    def GetContext(self) -> Context:
        return self.ContextInstance

    def GetAspiratePipettingDeviceTracker(self):
        return self.AspiratePipettingDeviceTrackerInstance

    def GetDispensePipettingDeviceTracker(self):
        return self.DispensePipettingDeviceTrackerInstance

    def Process(self):
        pass
