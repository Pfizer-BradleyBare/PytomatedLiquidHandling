from ....Tools.AbstractClasses import UniqueObjectABC
from ...Labware import LabwareTracker
from .Interface.ClosedContainerInterface import ClosedContainerInterface
from ....Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


class ClosedContainer(UniqueObjectABC, ClosedContainerInterface):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        ToolSequence: str,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        ClosedContainerInterface.__init__(self, BackendInstance, CustomErrorHandling)
        self.ToolSequence: str = ToolSequence
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )
