from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from ..Pipette import TransferOptions
from .BasePipette import LiquidClassCategoryTracker, Pipette, PipetteTipTracker


class HamiltonCORE96Head(Pipette):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        SupportedTipTrackerInstance: PipetteTipTracker,
        SupportedLabwareTrackerInstance: LabwareTracker,
        SupportedDeckLocationTrackerInstance: DeckLocationTracker,
        SupportedLiquidClassCategoryTrackerInstance: LiquidClassCategoryTracker,
    ):
        Pipette.__init__(
            self,
            UniqueIdentifier,
            BackendInstance,
            CustomErrorHandling,
            SupportedTipTrackerInstance,
            SupportedLabwareTrackerInstance,
            SupportedDeckLocationTrackerInstance,
            SupportedLiquidClassCategoryTrackerInstance,
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
