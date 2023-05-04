from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from ...Driver.Tools.AbstractOptions import AdvancedSingleOptionsABC
from ..Labware import LabwareTracker
from .BaseClosedContainer import ClosedContainer, OpenCloseOptionsTracker


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
        AdvancedOptionsInstance: FlipTubeDriver.Initialize.AdvancedOptions = FlipTubeDriver.Initialize.AdvancedOptions(),
    ):
        FlipTubeDriver.Initialize.Command(
            FlipTubeDriver.Initialize.Options(
                AdvancedOptionsInstance=FlipTubeDriver.Initialize.AdvancedOptions().UpdateOptions(
                    AdvancedOptionsInstance
                )
            )
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
        OpenCloseOptionsTrackerInstance: OpenCloseOptionsTracker,
        *,
        AdvancedOptionsInstance: FlipTubeDriver.Open.AdvancedOptions = FlipTubeDriver.Open.AdvancedOptions(),
        AdvancedOptionsTrackerInstance: FlipTubeDriver.Open.AdvancedOptionsTracker = FlipTubeDriver.Open.AdvancedOptionsTracker(),
    ):
        OptionsTrackerInstance = FlipTubeDriver.Open.OptionsTracker(
            ToolSequence=self.ToolSequence,
            AdvancedOptionsTrackerInstance=FlipTubeDriver.Open.AdvancedOptionsTracker().UpdateOptions(
                AdvancedOptionsTrackerInstance
            ),
        )
        for OpenCloseOptions in OpenCloseOptionsTrackerInstance.GetObjectsAsList():
            if (
                OpenCloseOptions.LayoutItemInstance.LabwareInstance
                in self.SupportedLabwareTrackerInstance.GetObjectsAsList()
            ):
                OptionsTrackerInstance.LoadSingle(
                    FlipTubeDriver.Open.Options(
                        Sequence=OpenCloseOptions.LayoutItemInstance.Sequence,
                        SequencePosition=OpenCloseOptions.Position,
                        AdvancedOptionsInstance=AdvancedOptionsInstance,
                    )
                )

        try:
            FlipTubeDriver.Open.Command(OptionsTrackerInstance).Execute()

        except:
            ...

    def Close(
        self,
        OpenCloseOptionsTrackerInstance: OpenCloseOptionsTracker,
        *,
        AdvancedOptionsInstance: FlipTubeDriver.CloseSpecial.AdvancedOptions = FlipTubeDriver.CloseSpecial.AdvancedOptions(),
        AdvancedOptionsTrackerInstance: FlipTubeDriver.CloseSpecial.AdvancedOptionsTracker = FlipTubeDriver.CloseSpecial.AdvancedOptionsTracker(),
    ):
        OptionsTrackerInstance = FlipTubeDriver.CloseSpecial.OptionsTracker(
            ToolSequence=self.ToolSequence,
            AdvancedOptionsTrackerInstance=FlipTubeDriver.CloseSpecial.AdvancedOptionsTracker().UpdateOptions(
                AdvancedOptionsTrackerInstance
            ),
        )
        for OpenCloseOptions in OpenCloseOptionsTrackerInstance.GetObjectsAsList():
            if (
                OpenCloseOptions.LayoutItemInstance.LabwareInstance
                in self.SupportedLabwareTrackerInstance.GetObjectsAsList()
            ):
                OptionsTrackerInstance.LoadSingle(
                    FlipTubeDriver.CloseSpecial.Options(
                        Sequence=OpenCloseOptions.LayoutItemInstance.Sequence,
                        SequencePosition=OpenCloseOptions.Position,
                        AdvancedOptionsInstance=AdvancedOptionsInstance,
                    )
                )

        try:
            FlipTubeDriver.CloseSpecial.Command(OptionsTrackerInstance).Execute()

        except:
            ...
