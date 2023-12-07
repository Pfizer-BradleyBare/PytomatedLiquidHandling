from typing import DefaultDict, Literal

from PytomatedLiquidHandling.Driver.Hamilton import Backend, FlipTubeTool
from PytomatedLiquidHandling.HAL import LayoutItem

from .Base import CloseableContainerABC, OpenCloseOptions


class HamiltonFlipTubeLandscape(CloseableContainerABC):
    """FlipTubes are a 1500uL conical tube that can be opened and closed on deck with a tool.

    This device only supports FlipTubes in the landscape orientation.

    Attributes:
        Backend: Only Hamilton backends are supported
        BackendErrorHandling: User handling is not possible for fliptubes.
        ToolLabwareID: The labware ID of the fliptube tool. Typically available on deck as a set of 4 tools.
    """

    Backend: Backend.HamiltonBackendABC
    BackendErrorHandling: Literal["N/A"] = "N/A"

    ToolLabwareID: str

    def Initialize(self):
        CloseableContainerABC.Initialize(self)

        Command = FlipTubeTool.Initialize.Command(
            Options=FlipTubeTool.Initialize.Options(
                ToolOrientation=FlipTubeTool.Initialize.Options.ToolOrientationOptions.Landscape
            )
        )
        self.Backend.ExecuteCommand(Command)
        self.Backend.WaitForResponseBlocking(Command)
        self.Backend.GetResponse(Command, FlipTubeTool.Initialize.Response)

    def Open(
        self,
        Options: list[OpenCloseOptions],
    ):
        Command = FlipTubeTool.ToolsPickUp.Command(
            Options=FlipTubeTool.ToolsPickUp.ListedOptions(LabwareID=self.ToolLabwareID)
        )
        Command.Options += [
            FlipTubeTool.ToolsPickUp.Options(ChannelNumber=i) for i in range(1, 5)
        ]
        # There are only 4 tools total so we will pick them all up.
        self.Backend.ExecuteCommand(Command)
        self.Backend.WaitForResponseBlocking(Command)
        self.Backend.GetResponse(Command, FlipTubeTool.ToolsPickUp.Response)
        # Pickup

        LayoutItemKeys: dict[str, LayoutItem.Plate] = {
            Opt.LayoutItem.Identifier: Opt.LayoutItem for Opt in Options
        }
        LayoutItemPositions = DefaultDict(list)
        # Open

        for Opt in Options:
            LayoutItemPositions[Opt.LayoutItem.Identifier].append(Opt.Position)
        # Collect positions organized by layout item

        for Key in LayoutItemPositions:
            Groups = LayoutItemKeys[Key].Labware.Wells.Layout.GroupPositionsColumnwise(
                LayoutItemPositions[Key]
            )

            LayoutItemPositions[Key] = [
                Group[i : i + 4] for Group in Groups for i in range(0, len(Group), 4)
            ]
            # Max number in each group is 4. Truncate them here just in case
        # Sort columnwise because the fliptube tool orientation is landscape. Meaning most efficient
        # open is along the columns

        for Key in LayoutItemPositions:
            for Group in LayoutItemPositions[Key]:
                Command = FlipTubeTool.FlipTubeOpen.Command(Options=list())
                for Index, PosID in enumerate(Group):
                    Command.Options.append(
                        FlipTubeTool.FlipTubeOpen.Options(
                            LabwareID=LayoutItemKeys[Key].LabwareID,
                            PositionID=PosID,
                            ChannelNumber=Index + 1,
                        )
                    )
                self.Backend.ExecuteCommand(Command)
                self.Backend.WaitForResponseBlocking(Command)
                self.Backend.GetResponse(Command, FlipTubeTool.FlipTubeOpen.Response)
        # Do the pickup. Each group contains 4 positions which correspond to each of 4 picked up tools.
        # It is possible that the group contains 1-4 posiitons. It should not matter.

        Command = FlipTubeTool.ToolsEject.Command(
            Options=FlipTubeTool.ToolsEject.Options(LabwareID=self.ToolLabwareID)
        )
        self.Backend.ExecuteCommand(Command)
        self.Backend.WaitForResponseBlocking(Command)
        self.Backend.GetResponse(Command, FlipTubeTool.ToolsEject.Response)

    def TimeToOpen(
        self,
        Options: list[OpenCloseOptions],
    ) -> float:
        return 0

    def Close(
        self,
        Options: list[OpenCloseOptions],
    ):
        Command = FlipTubeTool.ToolsPickUp.Command(
            Options=FlipTubeTool.ToolsPickUp.ListedOptions(LabwareID=self.ToolLabwareID)
        )
        Command.Options += [
            FlipTubeTool.ToolsPickUp.Options(ChannelNumber=i) for i in range(1, 5)
        ]
        # There are only 4 tools total so we will pick them all up.
        self.Backend.ExecuteCommand(Command)
        self.Backend.WaitForResponseBlocking(Command)
        self.Backend.GetResponse(Command, FlipTubeTool.ToolsPickUp.Response)
        # Pickup

        LayoutItemKeys: dict[str, LayoutItem.Plate] = {
            Opt.LayoutItem.Identifier: Opt.LayoutItem for Opt in Options
        }
        LayoutItemPositions = DefaultDict(list)
        # Open

        for Opt in Options:
            LayoutItemPositions[Opt.LayoutItem.Identifier].append(Opt.Position)
        # Collect positions organized by layout item

        for Key in LayoutItemPositions:
            Groups = LayoutItemKeys[Key].Labware.Wells.Layout.GroupPositionsColumnwise(
                LayoutItemPositions[Key]
            )

            LayoutItemPositions[Key] = [
                Group[i : i + 4] for Group in Groups for i in range(0, len(Group), 4)
            ]
            # Max number in each group is 4. Truncate them here just in case
        # Sort columnwise because the fliptube tool orientation is landscape. Meaning most efficient
        # open is along the columns

        for Key in LayoutItemPositions:
            for Group in LayoutItemPositions[Key]:
                Command = FlipTubeTool.FlipTubeClose.Command(Options=list())
                for Index, PosID in enumerate(Group):
                    Command.Options.append(
                        FlipTubeTool.FlipTubeClose.Options(
                            LabwareID=LayoutItemKeys[Key].LabwareID,
                            PositionID=PosID,
                            ChannelNumber=Index + 1,
                        )
                    )
                self.Backend.ExecuteCommand(Command)
                self.Backend.WaitForResponseBlocking(Command)
                self.Backend.GetResponse(Command, FlipTubeTool.FlipTubeClose.Response)
        # Do the pickup. Each group contains 4 positions which correspond to each of 4 picked up tools.
        # It is possible that the group contains 1-4 posiitons. It should not matter.

        Command = FlipTubeTool.ToolsEject.Command(
            Options=FlipTubeTool.ToolsEject.Options(LabwareID=self.ToolLabwareID)
        )
        self.Backend.ExecuteCommand(Command)
        self.Backend.WaitForResponseBlocking(Command)
        self.Backend.GetResponse(Command, FlipTubeTool.ToolsEject.Response)

    def TimeToClose(
        self,
        Options: list[OpenCloseOptions],
    ) -> float:
        return 0
