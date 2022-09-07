from .DeckLocation import DeckLocationTracker
from .FlipTube import FlipTubeTracker
from .Labware import LabwareTracker
from .Layout import LayoutTracker
from .Lid import LidTracker
from .MagneticRack import MagneticRackTracker
from .Notify import NotifyTracker
from .Pipette import PipetteTracker
from .TempControlDevice import TempControlDeviceTracker
from .Tip import TipTracker
from .Transport import TransportTracker


class Hal:
    def __init__(
        self,
        DeckLocationTrackerInstance: DeckLocationTracker,
        FlipTubeTrackerInstance: FlipTubeTracker,
        LabwareTrackerInstance: LabwareTracker,
        LayoutTrackerInstance: LayoutTracker,
        LidTrackerInstance: LidTracker,
        MagneticRackTrackerInstance: MagneticRackTracker,
        NotifyTrackerInstance: NotifyTracker,
        PipetteTrackerInstance: PipetteTracker,
        TempControlDeviceTrackerInstance: TempControlDeviceTracker,
        TipTrackerInstance: TipTracker,
        TransportTrackerInstance: TransportTracker,
    ):
        self.DeckLocationTrackerInstance: DeckLocationTracker = (
            DeckLocationTrackerInstance
        )
        self.FlipTubeTrackerInstance: FlipTubeTracker = FlipTubeTrackerInstance
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
        self.LayoutTrackerInstance: LayoutTracker = LayoutTrackerInstance
        self.LidTrackerInstance: LidTracker = LidTrackerInstance
        self.MagneticRackTrackerInstance: MagneticRackTracker = (
            MagneticRackTrackerInstance
        )
        self.NotifyTrackerInstance: NotifyTracker = NotifyTrackerInstance
        self.PipetteTrackerInstance: PipetteTracker = PipetteTrackerInstance
        self.TempControlDeviceTrackerInstance: TempControlDeviceTracker = (
            TempControlDeviceTrackerInstance
        )
        self.TipTrackerInstance: TipTracker = TipTrackerInstance
        self.TransportTrackerInstance: TransportTracker = TransportTrackerInstance

        def GetDeckLocationTracker(self) -> DeckLocationTracker:
            return self.DeckLocationTrackerInstance

        def GetFlipTubeTracker(self) -> FlipTubeTracker:
            return self.FlipTubeTrackerInstance

        def GetLabwareTracker(self) -> LabwareTracker:
            return self.LabwareTrackerInstance

        def GetLayoutTracker(self) -> LayoutTracker:
            return self.LayoutTrackerInstance

        def GetLidTracker(self) -> LidTracker:
            return self.LidTrackerInstance

        def GetMagneticRackTracker(self) -> MagneticRackTracker:
            return self.MagneticRackTrackerInstance

        def GetNotifyTracker(self) -> NotifyTracker:
            return self.NotifyTrackerInstance

        def GetPipetteTracker(self) -> PipetteTracker:
            return self.PipetteTrackerInstance

        def GetTempControlDeviceTracker(self) -> TempControlDeviceTracker:
            return self.TempControlDeviceTrackerInstance

        def GetTipTracker(self) -> TipTracker:
            return self.TipTrackerInstance

        def GetTransportTracker(self) -> TransportTracker:
            return self.TransportTrackerInstance
