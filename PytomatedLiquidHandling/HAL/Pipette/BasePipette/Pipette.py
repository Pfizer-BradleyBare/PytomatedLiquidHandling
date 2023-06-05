from ....Tools.AbstractClasses import UniqueObjectABC
from ...Labware import LabwareTracker
from .PipetteTip.PipetteTipTracker import PipetteTipTracker
from .Interface import TransferOptions
from ...Tools.AbstractClasses import InterfaceABC
from ...DeckLocation import DeckLocationTracker
from ....Driver.Tools.AbstractClasses import BackendABC
from abc import abstractmethod


class Pipette(UniqueObjectABC, InterfaceABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: BackendABC,
        CustomErrorHandling: bool,
        SupportedPipetteTipTrackerInstance: PipetteTipTracker,
        SupportedLabwareTrackerInstance: LabwareTracker,
        SupportedDeckLocationTrackerInstance: DeckLocationTracker,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        InterfaceABC.__init__(self, BackendInstance, CustomErrorHandling)
        self.SupportedPipetteTipTrackerInstance: PipetteTipTracker = (
            SupportedPipetteTipTrackerInstance
        )
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )
        self.SupportedDeckLocationTrackerInstance: DeckLocationTracker = (
            SupportedDeckLocationTrackerInstance
        )

    def LabwaresSupported(
        self,
        LabwareInstances: list[Labware],
    ) -> bool:
        ...

    @abstractmethod
    def Transfer(
        self,
        TransferOptionsTrackerInstance: TransferOptions.OptionsTracker,
    ):
        ...
