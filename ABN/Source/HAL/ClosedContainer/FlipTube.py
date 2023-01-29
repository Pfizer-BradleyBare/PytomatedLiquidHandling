from ...Driver.ClosedContainer import FlipTube as FlipTubeDriver
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

        FlipTubeDriver.InitializeCommand(
            "", FlipTubeDriver.InitializeOptions(""), True
        ).Execute()

    def Deinitialize(
        self,
    ):
        ...

    def Open(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
    ):

        OpenOptionsTrackerInstance = FlipTubeDriver.OpenOptionsTracker()
        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            OpenOptionsTrackerInstance.ManualLoad(
                FlipTubeDriver.OpenOptions(
                    "", self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        try:
            FlipTubeDriver.OpenCommand("", OpenOptionsTrackerInstance, True).Execute()

        except:
            ...

    def Close(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
    ):
        CloseOptionsTrackerInstance = FlipTubeDriver.CloseOptionsTracker()

        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            CloseOptionsTrackerInstance.ManualLoad(
                FlipTubeDriver.CloseOptions(
                    "", self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        try:
            FlipTubeDriver.CloseCommand("", CloseOptionsTrackerInstance, True).Execute()

        except:
            ...
