from dataclasses import dataclass

from PytomatedLiquidHandling.HAL.ClosedContainer.BaseClosedContainer.ClosedContainerABC import (
    ClosedContainerInterfaceCommand,
)

from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from .BaseClosedContainer import ClosedContainerABC


@dataclass
class HamiltonFlipTube(ClosedContainerABC):
    def _Initialize(self):
        ClosedContainerABC._Initialize(self)

        Command = FlipTubeDriver.Initialize.Command(
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(Command)
        self.BackendInstance.WaitForResponseBlocking(Command)
        self.BackendInstance.GetResponse(Command, FlipTubeDriver.Initialize.Response)

    def _Open(self, OptionsTrackerInstance: ClosedContainerABC.Open.OptionsTracker):
        OpenOptionsTrackerInstance = FlipTubeDriver.Open.OptionsTracker(
            ToolSequence=self.ToolSequence
        )
        for OpenCloseOptions in OptionsTrackerInstance.GetObjectsAsList():
            if (
                OpenCloseOptions.LayoutItemInstance.LabwareInstance
                in self.SupportedLabwareTrackerInstance.GetObjectsAsList()
            ):
                OpenOptionsTrackerInstance.LoadSingle(
                    FlipTubeDriver.Open.Options(
                        Sequence=OpenCloseOptions.LayoutItemInstance.Sequence,
                        SequencePosition=OpenCloseOptions.Position,
                    )
                )

        Command = FlipTubeDriver.Open.Command(
            OptionsTrackerInstance=OpenOptionsTrackerInstance,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(Command)
        self.BackendInstance.WaitForResponseBlocking(Command)
        self.BackendInstance.GetResponse(Command, FlipTubeDriver.Open.Response)

    def _OpenTime(
        self, OptionsTrackerInstance: ClosedContainerABC.Open.OptionsTracker
    ) -> float:
        return 0

    def _Close(self, OptionsTrackerInstance: ClosedContainerABC.Close.OptionsTracker):
        CloseOptionsTrackerInstance = FlipTubeDriver.Close.OptionsTracker(
            ToolSequence=self.ToolSequence
        )
        for OpenCloseOptions in OptionsTrackerInstance.GetObjectsAsList():
            if (
                OpenCloseOptions.LayoutItemInstance.LabwareInstance
                in self.SupportedLabwareTrackerInstance.GetObjectsAsList()
            ):
                CloseOptionsTrackerInstance.LoadSingle(
                    FlipTubeDriver.Close.Options(
                        Sequence=OpenCloseOptions.LayoutItemInstance.Sequence,
                        SequencePosition=OpenCloseOptions.Position,
                    )
                )

        Command = FlipTubeDriver.Close.Command(
            OptionsTrackerInstance=CloseOptionsTrackerInstance,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(Command)
        self.BackendInstance.WaitForResponseBlocking(Command)
        self.BackendInstance.GetResponse(Command, FlipTubeDriver.Close.Response)

    def _CloseTime(
        self, OptionsTrackerInstance: ClosedContainerABC.Close.OptionsTracker
    ) -> float:
        return 0
