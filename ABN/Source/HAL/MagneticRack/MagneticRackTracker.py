from ...Tools.AbstractClasses import UniqueItemTrackerABC
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from ..Pipette import PipetteTracker
from ..Tip import TipTracker
from .MagneticRack import MagneticRack


class MagneticRackTracker(UniqueItemTrackerABC[MagneticRack]):
    def __init__(
        self,
        LabwareTrackerInstance: LabwareTracker,
        DeckLocationTrackerInstance: DeckLocationTracker,
        PipetteDeviceTrackerInstance: PipetteTracker,
        TipTrackerInstance: TipTracker,
    ):
        UniqueItemTrackerABC.__init__(self)
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
        self.DeckLocationTrackerInstance: DeckLocationTracker = (
            DeckLocationTrackerInstance
        )
        self.PipetteDeviceTrackerInstance: PipetteTracker = PipetteDeviceTrackerInstance
        self.TipTrackerInstance: TipTracker = TipTrackerInstance


#
#
# End Class Definitions
#
#
