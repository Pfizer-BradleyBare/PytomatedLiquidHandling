from __future__ import annotations

from typing import Annotated, DefaultDict

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.driver.HAMILTON import FlipTubeTool
from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.hal import backend, layout_item

from .closeable_container_base import *
from .closeable_container_base import CloseableContainerBase
from .options import OpenCloseOptions


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonFlipTubeLandscape(CloseableContainerBase):
    """Hamilton FlipTubes are a special, Hamilton compatible, 1500uL conical tube that can be opened and closed on deck with a FlipTube tool.

    This device only supports FlipTubes in the landscape orientation.
    """

    backend: Annotated[HamiltonBackendBase, BeforeValidator(backend.validate_instance)]
    """Only Hamilton backends are supported."""

    tool_labware_id: str
    """The labware id of the FlipTube tool."""

    def initialize(self: HamiltonFlipTubeLandscape) -> None:
        """Executes the Hamilton FlipTubeTool Initialize command in the landscape orientation."""
        command = FlipTubeTool.Initialize.Command(
            options=FlipTubeTool.Initialize.Options(
                ToolOrientation=FlipTubeTool.Initialize.ToolOrientationOptions.Landscape,
            ),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, FlipTubeTool.Initialize.Response)

    def deinitialize(self: HamiltonFlipTubeLandscape) -> None:
        """No deinitialization actions are executed."""

    def open(
        self: HamiltonFlipTubeLandscape,
        options: list[OpenCloseOptions],
    ) -> None:
        """Hamilton FlipTube tool supports a max of 4 tools in use simultaneously in the driver.
        Thus, the function will sort the desired open positions then creates groups of 4 to open.
        """
        self.assert_supported_labware([item.layout_item.labware for item in options])
        self.assert_supported_deck_locations(
            [item.layout_item.deck_location for item in options],
        )

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
            opt.layout_item.identifier: opt.layout_item for opt in options
        }
        layout_item_positions = DefaultDict(list)
        # Open

        for opt in options:
            layout_item_positions[opt.layout_item.identifier].append(opt.position)
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
        # Do the open. Each group contains 4 positions which correspond to each of 4 picked up tools.
        # It is possible that the group contains 1-4 posiitons. It should not matter.

        command = FlipTubeTool.ToolsEject.Command(
            options=FlipTubeTool.ToolsEject.Options(LabwareID=self.tool_labware_id),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, FlipTubeTool.ToolsEject.Response)

    def open_time(
        self: HamiltonFlipTubeLandscape,
        options: list[OpenCloseOptions],
    ) -> float:
        """TODO"""
        self.assert_supported_labware([item.layout_item.labware for item in options])
        self.assert_supported_deck_locations(
            [item.layout_item.deck_location for item in options],
        )
        return 0

    def close(
        self: HamiltonFlipTubeLandscape,
        options: list[OpenCloseOptions],
    ) -> None:
        """Hamilton FlipTube tool supports a max of 4 tools in use simultaneously in the driver.
        Thus, the function will sort the desired open positions then creates groups of 4 to open.
        """
        self.assert_supported_labware([item.layout_item.labware for item in options])
        self.assert_supported_deck_locations(
            [item.layout_item.deck_location for item in options],
        )

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
            opt.layout_item.identifier: opt.layout_item for opt in options
        }
        layout_item_positions = DefaultDict(list)
        # close

        for opt in options:
            layout_item_positions[opt.layout_item.identifier].append(opt.position)
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
        # close is along the columns

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
        # Do the close. Each group contains 4 positions which correspond to each of 4 picked up tools.
        # It is possible that the group contains 1-4 posiitons. It should not matter.

        command = FlipTubeTool.ToolsEject.Command(
            options=FlipTubeTool.ToolsEject.Options(LabwareID=self.tool_labware_id),
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, FlipTubeTool.ToolsEject.Response)

    def close_time(
        self: HamiltonFlipTubeLandscape,
        options: list[OpenCloseOptions],
    ) -> float:
        """TODO"""
        self.assert_supported_labware([item.layout_item.labware for item in options])
        self.assert_supported_deck_locations(
            [item.layout_item.deck_location for item in options],
        )
        return 0
