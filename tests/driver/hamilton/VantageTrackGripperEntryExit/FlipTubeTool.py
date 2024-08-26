from loguru import logger

from plh.device.hamilton_venus import FlipTubeTool
from plh.device.hamilton_venus.backend import VantageTrackGripperEntryExit


def main(backend: VantageTrackGripperEntryExit) -> None:
    logger.info(f"Executing main() from {__file__}")

    logger.info("Initialize")
    command = FlipTubeTool.Initialize.Command(
        options=FlipTubeTool.Initialize.Options(
            ToolOrientation=FlipTubeTool.Initialize.ToolOrientationOptions.Landscape,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, FlipTubeTool.Initialize.Response)

    logger.info("Pickup")

    command = FlipTubeTool.ToolsPickUp.Command(
        options=FlipTubeTool.ToolsPickUp.OptionsList(LabwareID="Tool_FlipTube_4"),
    )
    command.options.append(FlipTubeTool.ToolsPickUp.Options(ChannelNumber=1))
    command.options.append(FlipTubeTool.ToolsPickUp.Options(ChannelNumber=2))
    command.options.append(FlipTubeTool.ToolsPickUp.Options(ChannelNumber=3))
    command.options.append(FlipTubeTool.ToolsPickUp.Options(ChannelNumber=4))
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, FlipTubeTool.ToolsPickUp.Response)

    logger.info("Open")
    command = FlipTubeTool.FlipTubeOpen.Command(
        options=FlipTubeTool.FlipTubeOpen.OptionsList(
            LabwareID="SMP_CAR_32_FlipTubes_A02_0001",
        ),
    )
    command.options.append(
        FlipTubeTool.FlipTubeOpen.Options(
            PositionID="1",
            ChannelNumber=1,
        ),
    )
    command.options.append(
        FlipTubeTool.FlipTubeOpen.Options(
            PositionID="2",
            ChannelNumber=2,
        ),
    )
    command.options.append(
        FlipTubeTool.FlipTubeOpen.Options(
            PositionID="3",
            ChannelNumber=3,
        ),
    )
    command.options.append(
        FlipTubeTool.FlipTubeOpen.Options(
            PositionID="4",
            ChannelNumber=4,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, FlipTubeTool.FlipTubeOpen.Response)

    logger.info("Close")
    command = FlipTubeTool.FlipTubeClose.Command(
        options=FlipTubeTool.FlipTubeClose.OptionsList(
            LabwareID="SMP_CAR_32_FlipTubes_A02_0001"
        )
    )
    command.options.append(
        FlipTubeTool.FlipTubeClose.Options(
            PositionID="1",
            ChannelNumber=1,
        ),
    )
    command.options.append(
        FlipTubeTool.FlipTubeClose.Options(
            PositionID="2",
            ChannelNumber=2,
        ),
    )
    command.options.append(
        FlipTubeTool.FlipTubeClose.Options(
            PositionID="3",
            ChannelNumber=3,
        ),
    )
    command.options.append(
        FlipTubeTool.FlipTubeClose.Options(
            PositionID="4",
            ChannelNumber=4,
        ),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, FlipTubeTool.FlipTubeOpen.Response)

    logger.info("Eject")
    command = FlipTubeTool.ToolsEject.Command(
        options=FlipTubeTool.ToolsEject.Options(LabwareID="Tool_FlipTube_4"),
    )
    backend.execute(command)
    backend.wait(command)
    backend.acknowledge(command, FlipTubeTool.ToolsPickUp.Response)


if __name__ == "__main__":
    logger.enable("plh")

    backend = VantageTrackGripperEntryExit(
        identifier="Example Star",
        simulation_on=True,
    )

    backend.start()
    # Creates the backend so we can communicate with the Hamilton

    main(backend)

    input("Press <Enter> to quit.")

    backend.stop()
