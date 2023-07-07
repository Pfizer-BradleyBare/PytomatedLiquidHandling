from dataclasses import dataclass

from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from .BaseClosedContainer import ClosedContainerABC, OpenCloseOptions


@dataclass
class HamiltonFlipTubeSpecial(ClosedContainerABC):
    def Initialize(self):
        ClosedContainerABC.Initialize(self)

        Command = FlipTubeDriver.Initialize.Command(
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(Command)
        self.BackendInstance.WaitForResponseBlocking(Command)
        self.BackendInstance.GetResponse(Command, FlipTubeDriver.Initialize.Response)

    def Open(
        self,
        *,
        OpenCloseOptionsTrackerInstance: OpenCloseOptions.OptionsTracker,
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

        Command = FlipTubeDriver.Open.Command(
            OptionsTrackerInstance=OptionsTrackerInstance,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(Command)
        self.BackendInstance.WaitForResponseBlocking(Command)
        self.BackendInstance.GetResponse(Command, FlipTubeDriver.Open.Response)

    def Close(
        self,
        *,
        OpenCloseOptionsTrackerInstance: OpenCloseOptions.OptionsTracker,
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

        Command = FlipTubeDriver.CloseSpecial.Command(
            OptionsTrackerInstance=OptionsTrackerInstance,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(Command)
        self.BackendInstance.WaitForResponseBlocking(Command)
        self.BackendInstance.GetResponse(Command, FlipTubeDriver.CloseSpecial.Response)
