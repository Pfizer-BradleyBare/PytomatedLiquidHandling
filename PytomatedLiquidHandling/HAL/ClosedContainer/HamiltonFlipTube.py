from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from ...Driver.Tools.AbstractOptions import AdvancedSingleOptionsABC
from ..Labware import LabwareTracker
from ..LayoutItem.BaseLayoutItem import LayoutItem
from .BaseClosedContainer.ClosedContainer import ClosedContainer


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
        AdvancedOptionsInstance: FlipTubeDriver.Initialize.AdvancedOptions
        | None = None,
    ):
        FlipTubeDriver.Initialize.Command(
            FlipTubeDriver.Initialize.Options(
                AdvancedOptionsInstance=FlipTubeDriver.Initialize.AdvancedOptions()
                if AdvancedOptionsInstance is None
                else AdvancedOptionsInstance
            ),
            True,
        ).Execute()

    def Deinitialize(
        self,
        *,
        AdvancedOptionsInstance: AdvancedSingleOptionsABC = AdvancedSingleOptionsABC(
            False
        ),
    ):
        ...

    def Open(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
        *,
        AdvancedOptionsInstance: FlipTubeDriver.Open.AdvancedOptions = FlipTubeDriver.Open.AdvancedOptions(),
        AdvancedOptionsTrackerInstance: FlipTubeDriver.Open.AdvancedOptionsTracker = FlipTubeDriver.Open.AdvancedOptionsTracker(),
    ):
        OpenOptionsTrackerInstance = FlipTubeDriver.Open.OptionsTracker(
            ToolSequence=self.ToolSequence,
            AdvancedOptionsTrackerInstance=AdvancedOptionsTrackerInstance,
        )
        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            OpenOptionsTrackerInstance.LoadSingle(
                FlipTubeDriver.Open.Options(
                    Sequence=LayoutItemInstance.Sequence,
                    SequencePosition=Position,
                    AdvancedOptionsInstance=AdvancedOptionsInstance,
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
        *,
        AdvancedOptionsInstance: FlipTubeDriver.Close.AdvancedOptions | None = None,
        AdvancedOptionsTrackerInstance: FlipTubeDriver.Close.AdvancedOptionsTracker
        | None = None,
    ):
        CloseOptionsTrackerInstance = FlipTubeDriver.Close.OptionsTracker(
            ToolSequence=self.ToolSequence,
            AdvancedOptionsTrackerInstance=FlipTubeDriver.Close.AdvancedOptionsTracker(
                CustomErrorHandling=True
            )
            if AdvancedOptionsTrackerInstance is None
            else AdvancedOptionsTrackerInstance,
        )

        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            CloseOptionsTrackerInstance.LoadSingle(
                FlipTubeDriver.Close.Options(
                    Sequence=LayoutItemInstance.Sequence,
                    SequencePosition=Position,
                    AdvancedOptionsInstance=FlipTubeDriver.Close.AdvancedOptions()
                    if AdvancedOptionsInstance is None
                    else AdvancedOptionsInstance,
                )
            )

        try:
            FlipTubeDriver.Close.Command(CloseOptionsTrackerInstance, True).Execute()

        except:
            ...
