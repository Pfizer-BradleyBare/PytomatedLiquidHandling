from typing import cast

from ...Driver.ClosedContainers.FlipTube import (
    CloseCommand,
    CloseOptions,
    CloseOptionsTracker,
    InitializeCommand,
    InitializeOptions,
    OpenCommand,
    OpenOptions,
    OpenOptionsTracker,
)
from ...Driver.Handler.DriverHandler import DriverHandler
from ...Server.Globals.HandlerRegistry import GetDriverHandler
from ..Labware import LabwareTracker
from ..Layout import LayoutItem
from .BaseClosedContainers.ClosedContainers import (
    ClosedContainers,
    ClosedContainersTypes,
)


class FlipTube(ClosedContainers):
    def __init__(
        self, ToolSequence: str, SupportedLabwareTrackerInstance: LabwareTracker
    ):
        ClosedContainers.__init__(
            self,
            ClosedContainersTypes.FlipTube,
            ToolSequence,
            SupportedLabwareTrackerInstance,
        )

    def Initialize(self):
        __DriverHandlerInstance: DriverHandler = cast(DriverHandler, GetDriverHandler())

        __DriverHandlerInstance.ExecuteCommand(
            InitializeCommand("", True, InitializeOptions(""))
        )

    def Deinitialize(self):
        pass

    def Open(self, LayoutItemInstances: list[LayoutItem], Positions: list[int]):
        __DriverHandlerInstance: DriverHandler = cast(DriverHandler, GetDriverHandler())

        OpenOptionsTrackerInstance = OpenOptionsTracker()

        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            OpenOptionsTrackerInstance.ManualLoad(
                OpenOptions(
                    "", self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        __DriverHandlerInstance.ExecuteCommand(
            OpenCommand("", True, OpenOptionsTrackerInstance)
        )

    def Close(self, LayoutItemInstances: list[LayoutItem], Positions: list[int]):
        __DriverHandlerInstance: DriverHandler = cast(DriverHandler, GetDriverHandler())

        CloseOptionsTrackerInstance = CloseOptionsTracker()

        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            CloseOptionsTrackerInstance.ManualLoad(
                CloseOptions(
                    "", self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        __DriverHandlerInstance.ExecuteCommand(
            CloseCommand("", True, CloseOptionsTrackerInstance)
        )
