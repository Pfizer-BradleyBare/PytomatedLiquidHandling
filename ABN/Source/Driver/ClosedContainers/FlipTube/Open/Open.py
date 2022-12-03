from collections import defaultdict

from ....Tools.Command.Command import Command
from .OpenOptionsTracker import OpenOptionsTracker


class OpenCommand(Command):
    def __init__(self, Name: str, OptionsTrackerInstance: OpenOptionsTracker):
        Command.__init__(self, Name)
        self.OptionsTrackerInstance: OpenOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "FlipTube"

    def GetCommandName(self) -> str:
        return "Open"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = defaultdict(list)
        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        return OutputDict
