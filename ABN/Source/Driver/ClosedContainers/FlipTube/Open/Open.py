from collections import defaultdict

from ....Tools.Command.Command import Command
from .OpenOptionsTracker import OpenOptionsTracker


class OpenCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsTrackerInstance: OpenOptionsTracker,
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsTrackerInstance: OpenOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "FlipTube"

    def GetCommandName(self) -> str:
        return "Open"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = defaultdict(list)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling  # type:ignore
        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        return OutputDict
