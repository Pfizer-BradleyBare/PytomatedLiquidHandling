from ....HAL.ClosedContainer import ClosedContainerTracker
from ....HAL.DeckLocation import DeckLocationTracker
from ....HAL.Labware import LabwareTracker
from ....HAL.Layout import LayoutItemGroupingTracker
from ....HAL.Lid import LidTracker

# from ....HAL.MagneticRack import MagneticRackTracker
from ....HAL.Notify import NotifyTracker
from ....HAL.Pipette import PipetteTracker
from ....HAL.TempControlDevice import TempControlDeviceTracker
from ....HAL.Tip import TipTracker
from ....HAL.TransportDevice import TransportDeviceTracker


class HALLayer:
    def __init__(self):
        self.DeckLocationTrackerInstance: DeckLocationTracker
        self.ClosedContainerTrackerInstance: ClosedContainerTracker
        self.LabwareTrackerInstance: LabwareTracker
        self.LayoutItemGroupingTrackerInstance: LayoutItemGroupingTracker
        self.LidTrackerInstance: LidTracker
        #   self.MagneticRackTrackerInstance: MagneticRackTracker
        self.NotifyTrackerInstance: NotifyTracker
        self.PipetteTrackerInstance: PipetteTracker
        self.TempControlDeviceTrackerInstance: TempControlDeviceTracker
        self.TipTrackerInstance: TipTracker
        self.TransportDeviceTrackerInstance: TransportDeviceTracker
