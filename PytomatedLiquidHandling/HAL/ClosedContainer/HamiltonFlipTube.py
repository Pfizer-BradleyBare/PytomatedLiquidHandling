from dataclasses import dataclass

from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from .Base import ClosedContainerABC


@dataclass
class HamiltonFlipTube(ClosedContainerABC):
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
        Options: list[ClosedContainerABC.Options],
    ):
        CommandOptions = FlipTubeDriver.Open.ListedOptions(
            ToolSequence=self.ToolSequence
        )
        for OpenCloseOptions in Options:
            if OpenCloseOptions.LayoutItem.Labware in self.SupportedLabwares:
                CommandOptions.append(
                    FlipTubeDriver.Open.Options(
                        FlipTubeSequence=OpenCloseOptions.LayoutItem.Sequence,
                        FlipTubeSequencePosition=OpenCloseOptions.Position,
                    )
                )

        Command = FlipTubeDriver.Open.Command(
            ListedOptions=CommandOptions,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(Command)
        self.BackendInstance.WaitForResponseBlocking(Command)
        self.BackendInstance.GetResponse(Command, FlipTubeDriver.Open.Response)

    def OpenTime(
        self,
        Options: list[ClosedContainerABC.Options],
    ) -> float:
        return 0

    def Close(
        self,
        Options: list[ClosedContainerABC.Options],
    ):
        CommandOptions = FlipTubeDriver.Close.ListedOptions(
            ToolSequence=self.ToolSequence
        )
        for OpenCloseOptions in Options:
            if OpenCloseOptions.LayoutItem.Labware in self.SupportedLabwares:
                CommandOptions.append(
                    FlipTubeDriver.Close.Options(
                        FlipTubeSequence=OpenCloseOptions.LayoutItem.Sequence,
                        FlipTubeSequencePosition=OpenCloseOptions.Position,
                    )
                )

        Command = FlipTubeDriver.Close.Command(
            ListedOptions=CommandOptions,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(Command)
        self.BackendInstance.WaitForResponseBlocking(Command)
        self.BackendInstance.GetResponse(Command, FlipTubeDriver.Close.Response)

    def CloseTime(
        self,
        Options: list[ClosedContainerABC.Options],
    ) -> float:
        return 0
