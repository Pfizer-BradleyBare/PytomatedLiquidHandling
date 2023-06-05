from ..Labware import LabwareTracker
from ..Pipette import TransferOptions
from .BasePipette import Pipette, PipetteTipTracker
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ..DeckLocation import DeckLocationTracker


class HamiltonCORE96Head(Pipette):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        SupportedPipetteTipTrackerInstance: PipetteTipTracker,
        SupportedLabwareTrackerInstance: LabwareTracker,
        SupportedDeckLocationTrackerInstance: DeckLocationTracker,
    ):
        Pipette.__init__(
            self,
            UniqueIdentifier,
            BackendInstance,
            CustomErrorHandling,
            SupportedPipetteTipTrackerInstance,
            SupportedLabwareTrackerInstance,
            SupportedDeckLocationTrackerInstance,
        )

    def Initialize(
        self,
    ):
        ...

    def Deinitialize(
        self,
    ):
        ...

    def Transfer(
        self,
        TransferOptionsTrackerInstance: TransferOptions.OptionsTracker,
    ):
        ...
