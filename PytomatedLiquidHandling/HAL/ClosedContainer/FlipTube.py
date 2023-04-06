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

        FlipTubeDriver.Initialize.Command(
            FlipTubeDriver.Initialize.Options(), True
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

        OpenOptionsTrackerInstance = FlipTubeDriver.Open.OptionsTracker()
        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            OpenOptionsTrackerInstance.ManualLoad(
                FlipTubeDriver.Open.Options(
                    self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        try:
            FlipTubeDriver.Open.Command(OpenOptionsTrackerInstance, True).Execute()

        except:
            ...

    def Close(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
    ):
        CloseOptionsTrackerInstance = FlipTubeDriver.Close.OptionsTracker()

        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            CloseOptionsTrackerInstance.ManualLoad(
                FlipTubeDriver.Close.Options(
                    self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        try:
            FlipTubeDriver.Close.Command(CloseOptionsTrackerInstance, True).Execute()

        except:
            ...
