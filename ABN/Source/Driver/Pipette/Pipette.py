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

    def Process(self):
        pass
