from __future__ import annotations

from typing import DefaultDict, Literal

from pydantic import dataclasses

from plh.driver.HAMILTON import FlipTubeTool
from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.hal import layout_item

from .closeable_container_base import *
from .closeable_container_base import CloseableContainerBase, OpenCloseOptions


@dataclasses.dataclass(kw_only=True)
class HamiltonFlipTubeLandscape(CloseableContainerBase):
    """FlipTubes are a 1500uL conical tube that can be opened and closed on deck with a tool.

    This device only supports FlipTubes in the landscape orientation.

    Attributes
    ----------
        Backend: Only Hamilton backends are supported
        BackendErrorHandling: User handling is not possible for fliptubes.
        ToolLabwareID: The labware ID of the fliptube tool. Typically available on deck as a set of 4 tools.
    """

    backend: HamiltonBackendBase
    backend_error_handling: Literal["N/A"] = "N/A"

    tool_labware_id: str

    def initialize(self: HamiltonFlipTubeLandscape) -> None:
        CloseableContainerBase.initialize(self)

        command = FlipTubeTool.Initialize.Command(
            options=FlipTubeTool.Initialize.Options(
                ToolOrientation=FlipTubeTool.Initialize.ToolOrientationOptions.Landscape,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, FlipTubeTool.Initialize.Response)

    def open(
        self: HamiltonFlipTubeLandscape,
        options: list[OpenCloseOptions],
    ) -> None:
        command = FlipTubeTool.ToolsPickUp.Command(
            options=FlipTubeTool.ToolsPickUp.OptionsList(
                LabwareID=self.tool_labware_id,
            ),
        )
        command.options += [
            FlipTubeTool.ToolsPickUp.Options(ChannelNumber=i) for i in range(1, 5)
        ]
        # There are only 4 tools total so we will pick them all up.
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, FlipTubeTool.ToolsPickUp.Response)
        # Pickup

        layout_item_keys: dict[str, layout_item.LayoutItemBase] = {
            opt.LayoutItem.identifier: opt.LayoutItem for opt in options
        }
        layout_item_positions = DefaultDict(list)
        # Open

        for opt in options:
            layout_item_positions[opt.LayoutItem.identifier].append(opt.Position)
        # Collect positions organized by layout item

        for key in layout_item_positions:
            groups = layout_item_keys[key].labware.layout.group_positions_columnwise(
                layout_item_positions[key],
            )

            layout_item_positions[key] = [
                group[i : i + 4] for group in groups for i in range(0, len(group), 4)
            ]
            # Max number in each group is 4. Truncate them here just in case
        # Sort columnwise because the fliptube tool orientation is landscape. Meaning most efficient
        # open is along the columns

        for key in layout_item_positions:
            for group in layout_item_positions[key]:
                command = FlipTubeTool.FlipTubeOpen.Command(options=[])
                for index, pos_id in enumerate(group):
                    command.options.append(
                        FlipTubeTool.FlipTubeOpen.Options(
                            LabwareID=layout_item_keys[key].labware_id,
                            PositionID=pos_id,
                            ChannelNumber=index + 1,
                        ),
                    )
                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, FlipTubeTool.FlipTubeOpen.Response)
        # Do the pickup. Each group contains 4 positions which correspond to each of 4 picked up tools.
        # It is possible that the group contains 1-4 posiitons. It should not matter.

        command = FlipTubeTool.ToolsEject.Command(
            options=FlipTubeTool.ToolsEject.Options(LabwareID=self.tool_labware_id),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, FlipTubeTool.ToolsEject.Response)

    def time_to_open(
        self: HamiltonFlipTubeLandscape,
        options: list[OpenCloseOptions],
    ) -> float:
        ...

    def close(
        self: HamiltonFlipTubeLandscape,
        options: list[OpenCloseOptions],
    ) -> None:
        command = FlipTubeTool.ToolsPickUp.Command(
            options=FlipTubeTool.ToolsPickUp.OptionsList(
                LabwareID=self.tool_labware_id,
            ),
        )
        command.options += [
            FlipTubeTool.ToolsPickUp.Options(ChannelNumber=i) for i in range(1, 5)
        ]
        # There are only 4 tools total so we will pick them all up.
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, FlipTubeTool.ToolsPickUp.Response)
        # Pickup

        layout_item_keys: dict[str, layout_item.LayoutItemBase] = {
            opt.LayoutItem.identifier: opt.LayoutItem for opt in options
        }
        layout_item_positions = DefaultDict(list)
        # Open

        for opt in options:
            layout_item_positions[opt.LayoutItem.identifier].append(opt.Position)
        # Collect positions organized by layout item

        for key in layout_item_positions:
            groups = layout_item_keys[key].labware.layout.group_positions_columnwise(
                layout_item_positions[key],
            )

            layout_item_positions[key] = [
                group[i : i + 4] for group in groups for i in range(0, len(group), 4)
            ]
            # Max number in each group is 4. Truncate them here just in case
        # Sort columnwise because the fliptube tool orientation is landscape. Meaning most efficient
        # open is along the columns

        for key in layout_item_positions:
            for group in layout_item_positions[key]:
                command = FlipTubeTool.FlipTubeClose.Command(options=[])
                for index, pos_id in enumerate(group):
                    command.options.append(
                        FlipTubeTool.FlipTubeClose.Options(
                            LabwareID=layout_item_keys[key].labware_id,
                            PositionID=pos_id,
                            ChannelNumber=index + 1,
                        ),
                    )
                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, FlipTubeTool.FlipTubeClose.Response)
        # Do the pickup. Each group contains 4 positions which correspond to each of 4 picked up tools.
        # It is possible that the group contains 1-4 posiitons. It should not matter.

        command = FlipTubeTool.ToolsEject.Command(
            options=FlipTubeTool.ToolsEject.Options(LabwareID=self.tool_labware_id),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, FlipTubeTool.ToolsEject.Response)

    def time_to_close(
        self: HamiltonFlipTubeLandscape,
        options: list[OpenCloseOptions],
    ) -> float:
        ...
