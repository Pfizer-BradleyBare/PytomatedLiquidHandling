from dataclasses import dataclass

from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from .Base import ClosedContainerABC, OpenCloseOptions


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
        Options: list[OpenCloseOptions],
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
        Options: list[OpenCloseOptions],
    ) -> float:
        return 0

    def Close(
        self,
        Options: list[OpenCloseOptions],
    ):
        CommandOptions = FlipTubeDriver.CloseSpecial.ListedOptions(
            ToolSequence=self.ToolSequence
        )
        for OpenCloseOptions in Options:
            if OpenCloseOptions.LayoutItem.Labware in self.SupportedLabwares:
                CommandOptions.append(
                    FlipTubeDriver.CloseSpecial.Options(
                        FlipTubeSequence=OpenCloseOptions.LayoutItem.Sequence,
                        FlipTubeSequencePosition=OpenCloseOptions.Position,
                    )
                )

        Command = FlipTubeDriver.CloseSpecial.Command(
            ListedOptions=CommandOptions,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(Command)
        self.BackendInstance.WaitForResponseBlocking(Command)
        self.BackendInstance.GetResponse(Command, FlipTubeDriver.CloseSpecial.Response)

    def CloseTime(
        self,
        Options: list[OpenCloseOptions],
    ) -> float:
        return 0
