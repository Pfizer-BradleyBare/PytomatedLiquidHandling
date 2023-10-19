from dataclasses import dataclass

from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from .Base import ClosedContainerABC, OpenCloseOptions


@dataclass
class HamiltonFlipTube(ClosedContainerABC):
    def Initialize(self):
        ClosedContainerABC.Initialize(self)

        Command = FlipTubeDriver.Initialize.Command(
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(Command)
        self.Backend.WaitForResponseBlocking(Command)
        self.Backend.GetResponse(Command, FlipTubeDriver.Initialize.Response)

    def Open(
        self,
        Options: list[OpenCloseOptions],
    ):
        CommandOptions = FlipTubeDriver.Open.ListedOptions(
            ToolLabwareID=self.ToolLabwareID, ToolPositionID=self.ToolPositionID
        )
        for OpenCloseOptions in Options:
            if OpenCloseOptions.LayoutItem.Labware in self.SupportedLabwares:
                CommandOptions.append(
                    FlipTubeDriver.Open.Options(
                        LabwareID=OpenCloseOptions.LayoutItem.LabwareID,
                        PositionID=OpenCloseOptions.LayoutItem.Labware.Wells.Addressing.GetPosition(
                            OpenCloseOptions.Position
                        ),
                    )
                )

        Command = FlipTubeDriver.Open.Command(
            ListedOptions=CommandOptions,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(Command)
        self.Backend.WaitForResponseBlocking(Command)
        self.Backend.GetResponse(Command, FlipTubeDriver.Open.Response)

    def OpenTime(
        self,
        Options: list[OpenCloseOptions],
    ) -> float:
        return 0

    def Close(
        self,
        Options: list[OpenCloseOptions],
    ):
        CommandOptions = FlipTubeDriver.Close.ListedOptions(
            ToolLabwareID=self.ToolLabwareID, ToolPositionID=self.ToolPositionID
        )
        for OpenCloseOptions in Options:
            if OpenCloseOptions.LayoutItem.Labware in self.SupportedLabwares:
                CommandOptions.append(
                    FlipTubeDriver.Close.Options(
                        LabwareID=OpenCloseOptions.LayoutItem.LabwareID,
                        PositionID=OpenCloseOptions.LayoutItem.Labware.Wells.Addressing.GetPosition(
                            OpenCloseOptions.Position
                        ),
                    )
                )

        Command = FlipTubeDriver.Close.Command(
            ListedOptions=CommandOptions,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(Command)
        self.Backend.WaitForResponseBlocking(Command)
        self.Backend.GetResponse(Command, FlipTubeDriver.Close.Response)

    def CloseTime(
        self,
        Options: list[OpenCloseOptions],
    ) -> float:
        return 0
