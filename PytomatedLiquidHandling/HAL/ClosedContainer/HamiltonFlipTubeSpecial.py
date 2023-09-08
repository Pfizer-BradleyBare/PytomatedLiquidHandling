from dataclasses import dataclass

from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from .Base import ClosedContainerABC


@dataclass
class HamiltonFlipTubeSpecial(ClosedContainerABC):
    def _Initialize(self):
        ClosedContainerABC._Initialize(self)

        Command = FlipTubeDriver.Initialize.Command(
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(Command)
        self.BackendInstance.WaitForResponseBlocking(Command)
        self.BackendInstance.GetResponse(Command, FlipTubeDriver.Initialize.Response)

    def _Open(
        self,
        Options: list[ClosedContainerABC.OpenCloseInterfaceCommand.Options],
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

    def _OpenTime(
        self,
        Options: list[ClosedContainerABC.OpenCloseInterfaceCommand.Options],
    ) -> float:
        return 0

    def _Close(
        self,
        Options: list[ClosedContainerABC.OpenCloseInterfaceCommand.Options],
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

    def _CloseTime(
        self,
        Options: list[ClosedContainerABC.OpenCloseInterfaceCommand.Options],
    ) -> float:
        return 0
