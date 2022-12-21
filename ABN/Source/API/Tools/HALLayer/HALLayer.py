from ....HAL.ClosedContainers.BaseClosedContainers import ClosedContainersTracker
from ....HAL.DeckLocation import DeckLocationTracker
from ....HAL.Labware import LabwareTracker
from ....HAL.Layout import LayoutItemGroupingTracker
from ....HAL.Lid import LidTracker

# from ....HAL.MagneticRack import MagneticRackTracker
from ....HAL.Notify import NotifyTracker
from ....HAL.Pipette.BasePipette import PipetteTracker
from ....HAL.TempControlDevice.BaseTempControlDevice import TempControlDeviceTracker
from ....HAL.Tip.BaseTip import TipTracker
from ....HAL.TransportDevice.BaseTransportDevice import TransportDeviceTracker


class HALLayer:
    def __init__(self):
        self.DeckLocationTrackerInstance: DeckLocationTracker
        self.ClosedContainersTrackerInstance: ClosedContainersTracker
        self.LabwareTrackerInstance: LabwareTracker
        self.LayoutItemGroupingTrackerInstance: LayoutItemGroupingTracker
        self.LidTrackerInstance: LidTracker
        #   self.MagneticRackTrackerInstance: MagneticRackTracker
        self.NotifyTrackerInstance: NotifyTracker
        self.PipetteTrackerInstance: PipetteTracker
        self.TempControlDeviceTrackerInstance: TempControlDeviceTracker
        self.TipTrackerInstance: TipTracker
        self.TransportDeviceTrackerInstance: TransportDeviceTracker
