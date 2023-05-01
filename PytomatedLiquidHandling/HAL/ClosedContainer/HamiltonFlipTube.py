from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from ..Labware import LabwareTracker
from ..LayoutItem.BaseLayoutItem import LayoutItem
from .BaseClosedContainer.ClosedContainer import ClosedContainer, ClosedContainerTypes


class HamiltonFlipTube(ClosedContainer):
    def __init__(
        self,
        UniqueIdentifier: str,
        ToolSequence: str,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        ClosedContainer.__init__(
            self,
            UniqueIdentifier,
            ToolSequence,
            SupportedLabwareTrackerInstance,
        )

    def Initialize(
        self,
        *,
        AdvancedOptionsInstance: FlipTubeDriver.Initialize.AdvancedOptions = FlipTubeDriver.Initialize.AdvancedOptions()
    ):
        FlipTubeDriver.Initialize.Command(
            FlipTubeDriver.Initialize.Options(
                AdvancedOptionsInstance=AdvancedOptionsInstance
            ),
            True,
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
                    ToolSequence=self.ToolSequence,
                    Sequence=LayoutItemInstance.Sequence,
                    SequencePosition=Position,
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
                    ToolSequence=self.ToolSequence,
                    Sequence=LayoutItemInstance.Sequence,
                    SequencePosition=Position,
                )
            )

        try:
            FlipTubeDriver.Close.Command(CloseOptionsTrackerInstance, True).Execute()

        except:
            ...
