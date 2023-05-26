from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from ..Labware import LabwareTracker
from .BaseClosedContainer import ClosedContainer, OpenCloseOptionsTracker
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


class HamiltonFlipTubeSpecial(ClosedContainer):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        ToolSequence: str,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        ClosedContainer.__init__(
            self,
            UniqueIdentifier,
            BackendInstance,
            CustomErrorHandling,
            ToolSequence,
            SupportedLabwareTrackerInstance,
        )

    def Initialize(self):
        FlipTubeDriver.Initialize.Command(
            OptionsInstance=FlipTubeDriver.Initialize.Options(),
            CustomErrorHandling=self.CustomErrorHandling,
        ).Execute()

    def Deinitialize(self):
        ...

    def Open(
        self,
        *,
        OpenCloseOptionsTrackerInstance: OpenCloseOptionsTracker,
    ):
        OptionsTrackerInstance = FlipTubeDriver.Open.OptionsTracker(
            ToolSequence=self.ToolSequence,
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
                    )
                )

        try:
            FlipTubeDriver.Open.Command(
                OptionsTrackerInstance=OptionsTrackerInstance,
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()

        except:
            ...

    def Close(
        self,
        *,
        OpenCloseOptionsTrackerInstance: OpenCloseOptionsTracker,
    ):
        OptionsTrackerInstance = FlipTubeDriver.CloseSpecial.OptionsTracker(
            ToolSequence=self.ToolSequence,
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
                    )
                )

        try:
            FlipTubeDriver.CloseSpecial.Command(
                OptionsTrackerInstance=OptionsTrackerInstance,
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()

        except:
            ...
