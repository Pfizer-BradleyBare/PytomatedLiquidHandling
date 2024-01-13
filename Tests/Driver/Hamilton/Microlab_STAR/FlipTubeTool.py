import os

from loguru import logger

from PytomatedLiquidHandling.Driver.Hamilton import FlipTubeTool
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR


def Main():
    logger.info(f"Executing Main() from {__file__}")

    logger.info(f"Initialize")
    Command = FlipTubeTool.Initialize.Command(
        Options=FlipTubeTool.Initialize.Options(
            ToolOrientation=FlipTubeTool.Initialize.Options.ToolOrientationOptions.Landscape
        )
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Backend.GetResponse(Command, FlipTubeTool.Initialize.Response)

    logger.info(f"Pickup")
    Command = FlipTubeTool.ToolsPickUp.Command(
        Options=FlipTubeTool.ToolsPickUp.ListedOptions(LabwareID="FlipTubeTools")
    )
    Command.Options.append(FlipTubeTool.ToolsPickUp.Options(ChannelNumber=1))
    Command.Options.append(FlipTubeTool.ToolsPickUp.Options(ChannelNumber=2))
    Command.Options.append(FlipTubeTool.ToolsPickUp.Options(ChannelNumber=3))
    Command.Options.append(FlipTubeTool.ToolsPickUp.Options(ChannelNumber=4))
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Backend.GetResponse(Command, FlipTubeTool.ToolsPickUp.Response)

    logger.info(f"Open")
    Command = FlipTubeTool.FlipTubeOpen.Command(Options=list())
    Command.Options.append(
        FlipTubeTool.FlipTubeOpen.Options(
            LabwareID="FlipTubes", PositionID="1", ChannelNumber=1
        )
    )
    Command.Options.append(
        FlipTubeTool.FlipTubeOpen.Options(
            LabwareID="FlipTubes", PositionID="2", ChannelNumber=2
        )
    )
    Command.Options.append(
        FlipTubeTool.FlipTubeOpen.Options(
            LabwareID="Plate_1", PositionID="A1", ChannelNumber=3
        )
    )
    Command.Options.append(
        FlipTubeTool.FlipTubeOpen.Options(
            LabwareID="FlipTubes", PositionID="4", ChannelNumber=4
        )
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Backend.GetResponse(Command, FlipTubeTool.FlipTubeOpen.Response)

    logger.info(f"Close")
    Command = FlipTubeTool.FlipTubeClose.Command(Options=list())
    Command.Options.append(
        FlipTubeTool.FlipTubeClose.Options(
            LabwareID="FlipTubes", PositionID="1", ChannelNumber=1
        )
    )
    Command.Options.append(
        FlipTubeTool.FlipTubeClose.Options(
            LabwareID="FlipTubes", PositionID="2", ChannelNumber=2
        )
    )
    Command.Options.append(
        FlipTubeTool.FlipTubeClose.Options(
            LabwareID="FlipTubes", PositionID="3", ChannelNumber=3
        )
    )
    Command.Options.append(
        FlipTubeTool.FlipTubeClose.Options(
            LabwareID="FlipTubes", PositionID="4", ChannelNumber=4
        )
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Backend.GetResponse(Command, FlipTubeTool.FlipTubeOpen.Response)

    logger.info(f"Eject")
    Command = FlipTubeTool.ToolsEject.Command(
        Options=FlipTubeTool.ToolsEject.Options(LabwareID="FlipTubeTools")
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Backend.GetResponse(Command, FlipTubeTool.ToolsPickUp.Response)


if __name__ == "__main__":
    logger.enable("PytomatedLiquidHandling")

    Backend = MicrolabSTAR(
        Identifier="Example Star",
        SimulationOn=True,
        DeckLayoutPath=os.path.join(os.path.dirname(__file__), "SimulationLayout.lay"),
    )
    Backend.StartBackend()
    # Creates the Backend so we can communicate with the Hamilton

    Main()

    input("Press <Enter> to quit.")

    Backend.StopBackend()
