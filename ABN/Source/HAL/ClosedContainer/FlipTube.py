from ...Driver.ClosedContainer.FlipTube import (
    CloseCommand,
    CloseOptions,
    CloseOptionsTracker,
    InitializeCommand,
    InitializeOptions,
    OpenCommand,
    OpenOptions,
    OpenOptionsTracker,
)
from ..Labware import LabwareTracker
from ..Layout import LayoutItem
from .BaseClosedContainer.ClosedContainer import ClosedContainer, ClosedContainerTypes


class FlipTube(ClosedContainer):
    def __init__(
        self, ToolSequence: str, SupportedLabwareTrackerInstance: LabwareTracker
    ):
        ClosedContainer.__init__(
            self,
            ClosedContainerTypes.FlipTube,
            ToolSequence,
            SupportedLabwareTrackerInstance,
        )

    def Initialize(
        self,
    ):

        InitializeCommand("", InitializeOptions(""), True).Execute()

    def Deinitialize(
        self,
    ):
        ...

    def Open(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
    ):

        OpenOptionsTrackerInstance = OpenOptionsTracker()
        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            OpenOptionsTrackerInstance.ManualLoad(
                OpenOptions(
                    "", self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        try:
            OpenCommand("", OpenOptionsTrackerInstance, True).Execute()

        except:
            ...

    def Close(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
    ):
        CloseOptionsTrackerInstance = CloseOptionsTracker()

        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            CloseOptionsTrackerInstance.ManualLoad(
                CloseOptions(
                    "", self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        try:
            CloseCommand("", CloseOptionsTrackerInstance, True).Execute()

        except:
            ...
