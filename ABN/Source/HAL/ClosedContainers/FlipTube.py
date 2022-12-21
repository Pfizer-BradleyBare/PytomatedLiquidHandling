from ...Driver.ClosedContainers.FlipTube import (
    CloseCommand,
    CloseOptions,
    CloseOptionsTracker,
    InitializeCommand,
    InitializeOptions,
    OpenCommand,
    OpenOptions,
    OpenOptionsTracker,
)
from ...Driver.Tools import CommandTracker
from ..Labware import LabwareTracker
from ..Layout import LayoutItem
from .BaseClosedContainers.ClosedContainers import (
    ClosedContainers,
    ClosedContainersTypes,
)


class FlipTube(ClosedContainers):
    def __init__(
        self, ToolSequence: str, SupportedLabwareTrackerInstance: LabwareTracker
    ):
        ClosedContainers.__init__(
            self,
            ClosedContainersTypes.FlipTube,
            ToolSequence,
            SupportedLabwareTrackerInstance,
        )

    def Initialize(self) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            InitializeCommand("", True, InitializeOptions(""))
        )

        return ReturnCommandTracker

    def Deinitialize(self) -> CommandTracker:
        return CommandTracker()

    def Open(
        self, LayoutItemInstances: list[LayoutItem], Positions: list[int]
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        OpenOptionsTrackerInstance = OpenOptionsTracker()
        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            OpenOptionsTrackerInstance.ManualLoad(
                OpenOptions(
                    "", self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        ReturnCommandTracker.ManualLoad(
            OpenCommand("", True, OpenOptionsTrackerInstance)
        )

        return ReturnCommandTracker

    def Close(
        self, LayoutItemInstances: list[LayoutItem], Positions: list[int]
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        CloseOptionsTrackerInstance = CloseOptionsTracker()

        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            CloseOptionsTrackerInstance.ManualLoad(
                CloseOptions(
                    "", self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        ReturnCommandTracker.ManualLoad(
            CloseCommand("", True, CloseOptionsTrackerInstance)
        )

        return ReturnCommandTracker
